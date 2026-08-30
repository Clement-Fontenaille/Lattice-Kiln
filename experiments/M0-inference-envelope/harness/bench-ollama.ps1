<#
.SYNOPSIS
  M0 - full matrix measurement via Ollama (runtime of record).

.DESCRIPTION
  Implements PROTOCOL.md for every model x quant x context-fill cell in
  models.json. Writes one JSON record per run to results/runs/.

  Uses Ollama's own timing fields (load_duration, prompt_eval_duration,
  eval_duration) rather than wall-clock stream timing - they are the numbers we
  want and are reported on every non-streamed response.

.NOTES
  Windows PowerShell 5.1 compatible. ASCII only.
  Requires Ollama running at http://localhost:11434. Models are pulled on demand
  unless -SkipPull is given. Untested until the runtime is installed.
#>

[CmdletBinding()]
param(
  [string] $ModelsJson = (Join-Path $PSScriptRoot 'models.json'),
  [string] $OutDir     = (Join-Path $PSScriptRoot '..\results'),
  [string] $ServerUrl  = 'http://localhost:11434',
  [switch] $SkipPull
)

$ErrorActionPreference = 'Stop'

# Ollama is installed per-user on this host and is not on PATH in a fresh shell.
# Self-locate it before any '& ollama' call below.
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
  $ollamaDir = Join-Path $env:LOCALAPPDATA 'Programs\Ollama'
  if (Test-Path (Join-Path $ollamaDir 'ollama.exe')) {
    $env:Path = "$ollamaDir;$env:Path"
  }
}
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
  throw "ollama.exe not found on PATH or at $env:LOCALAPPDATA\Programs\Ollama. Install Ollama or fix PATH."
}

$runsDir = Join-Path $OutDir 'runs'
if (-not (Test-Path $runsDir)) { New-Item -ItemType Directory -Path $runsDir -Force | Out-Null }

$cfg = Get-Content $ModelsJson -Raw | ConvertFrom-Json

$ollamaVersion = try { (& ollama --version) -join ' ' } catch { 'unknown' }

$hostRef = $null
$hostFile = Join-Path $OutDir 'host.json'
if (Test-Path $hostFile) {
  $bytes = [System.IO.File]::ReadAllBytes($hostFile)
  $hash  = [System.Security.Cryptography.SHA256]::Create().ComputeHash($bytes)
  $hostRef = -join ($hash | ForEach-Object { $_.ToString('x2') })
}

function Test-Server {
  try { Invoke-RestMethod -Uri "$ServerUrl/api/tags" -TimeoutSec 5 | Out-Null; return $true }
  catch { return $false }
}

function Get-InstalledTags {
  (Invoke-RestMethod -Uri "$ServerUrl/api/tags").models | ForEach-Object { $_.name }
}

function Ensure-Model([string] $Tag) {
  if ((Get-InstalledTags) -contains $Tag) { return }
  if ($SkipPull) { throw "Model '$Tag' not installed and -SkipPull set." }
  Write-Host "  pulling $Tag ..."
  & ollama pull $Tag
  if ($LASTEXITCODE -ne 0) { throw "ollama pull $Tag failed." }
}

$fillerUnit = "The system distributes reasoning across short-lived invocations so that no single call must hold the entire problem in working memory. "
function Get-PromptOfApproxTokens([int] $Tokens) {
  $targetChars = [math]::Max(40, $Tokens * 4)   # ~4 chars/token for Qwen on prose
  $sb = New-Object System.Text.StringBuilder
  while ($sb.Length -lt $targetChars) { [void]$sb.Append($fillerUnit) }
  "Summarize the following text in one sentence.`n`n" + $sb.ToString().Substring(0, $targetChars)
}

function Invoke-Gen {
  param([string] $Model, [string] $Prompt, [int] $NumCtx)
  $body = @{
    model      = $Model
    prompt     = $Prompt
    stream     = $false
    keep_alive = $cfg.ollama_options.keep_alive_bench
    options    = @{
      num_ctx     = $NumCtx
      num_predict = [int]$cfg.ollama_options.num_predict
      temperature = [double]$cfg.ollama_options.temperature
      seed        = [int]$cfg.ollama_options.seed
    }
  } | ConvertTo-Json -Depth 5
  Invoke-RestMethod -Uri "$ServerUrl/api/generate" -Method Post -Body $body -ContentType 'application/json' -TimeoutSec 900
}

function Unload-Model([string] $Model) {
  $sw = [System.Diagnostics.Stopwatch]::StartNew()
  $body = @{ model = $Model; prompt = ''; stream = $false; keep_alive = 0 } | ConvertTo-Json
  try { Invoke-RestMethod -Uri "$ServerUrl/api/generate" -Method Post -Body $body -ContentType 'application/json' -TimeoutSec 60 | Out-Null } catch {}
  for ($i = 0; $i -lt 60; $i++) {
    $ps = (Invoke-RestMethod -Uri "$ServerUrl/api/ps").models
    if (-not ($ps | Where-Object { $_.name -eq $Model })) { break }
    Start-Sleep -Milliseconds 250
  }
  $sw.Stop()
  return [int]$sw.ElapsedMilliseconds
}

function Get-Resident([string] $Model) {
  $m = (Invoke-RestMethod -Uri "$ServerUrl/api/ps").models | Where-Object { $_.name -eq $Model } | Select-Object -First 1
  if (-not $m) { return [pscustomobject]@{ size_mb = $null; size_vram_mb = $null } }
  [pscustomobject]@{
    size_mb      = [math]::Round($m.size / 1MB)
    size_vram_mb = [math]::Round($m.size_vram / 1MB)
  }
}

function NumCtxFor([int] $Fill) { if ($Fill -le 512) { 1024 } else { $Fill } }

function New-Record {
  param($Model, $Quant, $Fill, $Rep, $NumCtx, $Resp, $Resident, $Status, $Note, [bool]$IsCold, [bool]$Warmup)
  $md = [ordered]@{
    load_ms           = $null; prompt_eval_count = $null; prompt_eval_ms = $null
    eval_count        = $null; eval_ms = $null; prefill_tok_s = $null; gen_tok_s = $null
    gpu_layers        = $null; total_layers = $null
    size_mb           = $Resident.size_mb; vram_resident_mb = $Resident.size_vram_mb
  }
  if ($Resp) {
    $md.load_ms           = [math]::Round($Resp.load_duration / 1e6)
    $md.prompt_eval_count = $Resp.prompt_eval_count
    $md.prompt_eval_ms    = [math]::Round($Resp.prompt_eval_duration / 1e6)
    $md.eval_count        = $Resp.eval_count
    $md.eval_ms           = [math]::Round($Resp.eval_duration / 1e6)
    if ($Resp.prompt_eval_duration -gt 0) { $md.prefill_tok_s = [math]::Round($Resp.prompt_eval_count / ($Resp.prompt_eval_duration / 1e9), 2) }
    if ($Resp.eval_duration -gt 0)        { $md.gen_tok_s     = [math]::Round($Resp.eval_count / ($Resp.eval_duration / 1e9), 2) }
  }
  [ordered]@{
    schema = 'm0-run/1'; runtime = 'ollama'; runtime_version = $ollamaVersion
    model = $Model; quant = $Quant; context_fill = $Fill; num_ctx = $NumCtx
    repetition = $Rep; is_cold = $IsCold; warmup = $Warmup
    timestamp = (Get-Date).ToString('o'); host_ref = $hostRef
    metrics = $md; status = $Status; note = $Note
  }
}

function Save-Record($rec, [string] $Name) {
  $rec | ConvertTo-Json -Depth 6 | Set-Content -Path (Join-Path $runsDir $Name) -Encoding utf8
}
function Slug([string] $s) { $s -replace '[:/\\]', '-' }

# ------------------------------------------------------------------ main
if (-not (Test-Server)) { throw "Ollama not reachable at $ServerUrl. Start it and retry." }

foreach ($m in $cfg.models) {
  foreach ($qp in $m.ollama.PSObject.Properties) {
    $quant = $qp.Name
    $tag   = $qp.Value
    Write-Host ("== {0} {1}  ({2})" -f $m.family, $quant, $tag)
    try { Ensure-Model $tag } catch { Write-Warning $_; continue }

    # cold-load probe: one clean unload -> load
    Unload-Model $tag | Out-Null
    try {
      $r = Invoke-Gen -Model $tag -Prompt (Get-PromptOfApproxTokens 512) -NumCtx 1024
      Save-Record (New-Record $tag $quant 512 0 1024 $r (Get-Resident $tag) 'ok' 'cold-load probe' $true $true) `
                  ("ollama__{0}__{1}__coldload.json" -f (Slug $tag), $quant)
      Write-Host ("   cold load_ms={0}" -f [math]::Round($r.load_duration / 1e6))
    } catch {
      Save-Record (New-Record $tag $quant 512 0 1024 $null ([pscustomobject]@{size_mb=$null;size_vram_mb=$null}) 'error' "$_" $true $true) `
                  ("ollama__{0}__{1}__coldload.json" -f (Slug $tag), $quant)
      Write-Warning "cold load failed for ${tag}: $_"; continue
    }

    foreach ($fill in $cfg.context_fills) {
      if ($fill -gt $m.stated_max_context) {
        Save-Record (New-Record $tag $quant $fill 1 (NumCtxFor $fill) $null ([pscustomobject]@{size_mb=$null;size_vram_mb=$null}) 'skipped' 'fill exceeds stated_max_context' $false $false) `
                    ("ollama__{0}__{1}__{2}__skip.json" -f (Slug $tag), $quant, $fill)
        continue
      }
      $nctx = NumCtxFor $fill
      $reps = @(0) + $cfg.recorded_repetitions
      foreach ($rep in $reps) {
        try {
          $r = Invoke-Gen -Model $tag -Prompt (Get-PromptOfApproxTokens $fill) -NumCtx $nctx
          $res = Get-Resident $tag
          Save-Record (New-Record $tag $quant $fill $rep $nctx $r $res 'ok' '' $false ($rep -eq 0)) `
                      ("ollama__{0}__{1}__{2}__{3}.json" -f (Slug $tag), $quant, $fill, $rep)
          if ($rep -eq 1) {
            $pf = if ($r.prompt_eval_duration -gt 0) { [math]::Round($r.prompt_eval_count / ($r.prompt_eval_duration / 1e9), 1) } else { 0 }
            $gf = if ($r.eval_duration -gt 0) { [math]::Round($r.eval_count / ($r.eval_duration / 1e9), 1) } else { 0 }
            Write-Host ("   fill={0,6}  prefill={1,7} tok/s  gen={2,6} tok/s  vram={3} MB" -f $fill, $pf, $gf, $res.size_vram_mb)
          }
        } catch {
          $msg = "$_"
          $status = if ($msg -match 'memory|OOM|out of memory') { 'oom' } else { 'error' }
          Save-Record (New-Record $tag $quant $fill $rep $nctx $null ([pscustomobject]@{size_mb=$null;size_vram_mb=$null}) $status $msg $false ($rep -eq 0)) `
                      ("ollama__{0}__{1}__{2}__{3}.json" -f (Slug $tag), $quant, $fill, $rep)
          Write-Warning ("   fill={0} rep={1} -> {2}: {3}" -f $fill, $rep, $status, $msg)
          if ($status -eq 'oom') { break }
        }
      }
    }
    Unload-Model $tag | Out-Null
  }
}

# ------------------------------------------------------------------ switch cost
Write-Host "== switch-cost pass (Q4_K_M chain)"
$chain = @()
foreach ($m in $cfg.models) { if ($m.ollama.Q4_K_M) { $chain += [string]$m.ollama.Q4_K_M } }
if ($chain.Count -ge 2) {
  $chain += $chain[0]
  for ($i = 0; $i -lt $chain.Count - 1; $i++) {
    $from = $chain[$i]; $to = $chain[$i + 1]
    try {
      Unload-Model $from | Out-Null
      $unloadMs = Unload-Model $to        # target guaranteed absent; wall time of the unload path
      $r = Invoke-Gen -Model $to -Prompt (Get-PromptOfApproxTokens 512) -NumCtx 1024
      $loadMs = [math]::Round($r.load_duration / 1e6)
      $rec = [ordered]@{
        schema = 'm0-switch/1'; runtime = 'ollama'; runtime_version = $ollamaVersion
        from = $from; to = $to; unload_ms = $unloadMs; load_ms = $loadMs
        switch_ms = $unloadMs + $loadMs
        timestamp = (Get-Date).ToString('o'); host_ref = $hostRef
      }
      Save-Record $rec ("switch__{0}__to__{1}.json" -f (Slug $from), (Slug $to))
      Write-Host ("   {0} -> {1}   switch_ms={2}" -f $from, $to, $rec.switch_ms)
    } catch { Write-Warning "switch $from -> ${to}: $_" }
  }
}

Write-Host ""
Write-Host "Done. Records in: $runsDir"
Write-Host "Next: wsl bash harness/bench-llamacpp.sh   then   pwsh harness/aggregate.ps1"
