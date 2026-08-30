<#
.SYNOPSIS
  M0 - the two PROTOCOL.md metrics the matrix sweep does not cover:
  concurrent_delta (inference with the dev environment idle vs. active) and
  sustained_drift (generation rate at minute 1 vs. minute ~10).

.DESCRIPTION
  Runs against one representative cell (the expected working default:
  qwen2.5-coder 7B at Q5_K_M, 4k context) so the extra wall-clock stays bounded.
  Falls back to whatever model tag is passed / first installed if that tag is
  absent, so it can run on a partial set of pulls.

  concurrent_delta: 5 recorded reps idle, then 5 with a synthetic host load
  standing in for "VS Code + a language server + a build" - N CPU workers
  (N = logical processors) each spinning math and touching ~150 MB of RAM.
  This is a proxy, recorded as such in the run note; the FX-8300 is the
  contended resource either way.

  sustained_drift: back-to-back 320-token generations for -DriftMinutes minutes,
  one record each, tagged with elapsed seconds so aggregate.ps1 can compare the
  first minute against the last.

  Records land in results/runs/ with schemas m0-concurrent/1 and m0-drift/1.

.NOTES
  Windows PowerShell 5.1 compatible. ASCII only. Requires Ollama running.
#>

[CmdletBinding()]
param(
  [string] $OutDir      = (Join-Path $PSScriptRoot '..\results'),
  [string] $ServerUrl   = 'http://localhost:11434',
  [string] $ModelTag    = 'qwen2.5-coder:7b-instruct-q5_K_M',
  [string] $Quant       = 'Q5_K_M',
  [int]    $Fill        = 4096,
  [int]    $Reps        = 5,
  [int]    $DriftMinutes = 11,
  [switch] $SkipConcurrent,
  [switch] $SkipDrift
)

$ErrorActionPreference = 'Stop'

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
  $ollamaDir = Join-Path $env:LOCALAPPDATA 'Programs\Ollama'
  if (Test-Path (Join-Path $ollamaDir 'ollama.exe')) { $env:Path = "$ollamaDir;$env:Path" }
}

$runsDir = Join-Path $OutDir 'runs'
if (-not (Test-Path $runsDir)) { New-Item -ItemType Directory -Path $runsDir -Force | Out-Null }

$ollamaVersion = try { (& ollama --version) -join ' ' } catch { 'unknown' }
$hostRef = $null
$hostFile = Join-Path $OutDir 'host.json'
if (Test-Path $hostFile) {
  $bytes = [System.IO.File]::ReadAllBytes($hostFile)
  $hash  = [System.Security.Cryptography.SHA256]::Create().ComputeHash($bytes)
  $hostRef = -join ($hash | ForEach-Object { $_.ToString('x2') })
}

function Get-InstalledTags {
  (Invoke-RestMethod -Uri "$ServerUrl/api/tags").models | ForEach-Object { $_.name }
}

# Resolve the target tag: requested -> else first installed qwen2.5-coder -> else first installed.
$installed = @(Get-InstalledTags)
if ($installed.Count -eq 0) { throw "No models installed on $ServerUrl. Pull at least one first." }
if ($installed -notcontains $ModelTag) {
  $alt = $installed | Where-Object { $_ -like 'qwen2.5-coder*' } | Select-Object -First 1
  if (-not $alt) { $alt = $installed[0] }
  Write-Warning "Requested $ModelTag not installed; using $alt instead."
  $ModelTag = $alt
  $Quant = switch -Regex ($ModelTag) { 'q8_0' {'Q8_0'} 'q5_k_m' {'Q5_K_M'} 'q4_k_m' {'Q4_K_M'} default {'unknown'} }
}
Write-Host ("target: {0}  quant={1}  fill={2}" -f $ModelTag, $Quant, $Fill)

$fillerUnit = "In a constrained local system, an orchestrator decomposes a task, routes each piece to a short-lived processor, gathers evidence, and verifies results before integration. "
function Get-Prompt([int] $Tokens, [string] $Nonce) {
  $targetChars = [math]::Max(40, $Tokens * 4)
  $sb = New-Object System.Text.StringBuilder
  while ($sb.Length -lt $targetChars) { [void]$sb.Append($fillerUnit) }
  "[run $Nonce]`n`nContext (background reading):`n" + $sb.ToString().Substring(0, $targetChars) +
  "`n`nTask: Using the context above only as loose inspiration, write a long, thorough " +
  "engineering design note (aim for about 400 words) on how to build a reliable local AI " +
  "coding assistant on limited hardware. Use several paragraphs with headings. Write the full note now."
}

function Invoke-Gen([string] $Prompt, [int] $NumCtx, [int] $NumPredict = 320) {
  $body = @{
    model = $ModelTag; prompt = $Prompt; stream = $false; keep_alive = '5m'
    options = @{ num_ctx = $NumCtx; num_predict = $NumPredict; temperature = 0; seed = 1 }
  } | ConvertTo-Json -Depth 5
  Invoke-RestMethod -Uri "$ServerUrl/api/generate" -Method Post -Body $body -ContentType 'application/json' -TimeoutSec 900
}

function Get-Resident {
  $m = (Invoke-RestMethod -Uri "$ServerUrl/api/ps").models | Where-Object { $_.name -eq $ModelTag } | Select-Object -First 1
  if (-not $m) { return [pscustomobject]@{ size_mb=$null; size_vram_mb=$null } }
  [pscustomobject]@{ size_mb=[math]::Round($m.size/1MB); size_vram_mb=[math]::Round($m.size_vram/1MB) }
}

function Metrics-From($r) {
  $md = [ordered]@{
    load_ms=$null; prompt_eval_count=$null; prompt_eval_ms=$null; eval_count=$null
    eval_ms=$null; prefill_tok_s=$null; gen_tok_s=$null
  }
  if ($r) {
    $md.load_ms = [math]::Round($r.load_duration/1e6)
    $md.prompt_eval_count = $r.prompt_eval_count
    $md.prompt_eval_ms = [math]::Round($r.prompt_eval_duration/1e6)
    $md.eval_count = $r.eval_count
    $md.eval_ms = [math]::Round($r.eval_duration/1e6)
    if ($r.prompt_eval_duration -gt 0) { $md.prefill_tok_s = [math]::Round($r.prompt_eval_count/($r.prompt_eval_duration/1e9),2) }
    if ($r.eval_duration -gt 0)        { $md.gen_tok_s     = [math]::Round($r.eval_count/($r.eval_duration/1e9),2) }
  }
  $md
}

function Save-Record($rec, [string] $Name) {
  $rec | ConvertTo-Json -Depth 6 | Set-Content -Path (Join-Path $runsDir $Name) -Encoding utf8
}
function Slug([string] $s) { $s -replace '[:/\\]', '-' }

# --- synthetic host-load generator -------------------------------------------
# N CPU workers spinning FP math and touching ~150 MB each. Proxy for editor +
# language server + build tools competing with inference for the FX-8300.
function Start-HostLoad {
  $n = [int]$env:NUMBER_OF_PROCESSORS
  Write-Host ("   starting synthetic host load: {0} CPU workers" -f $n)
  1..$n | ForEach-Object {
    Start-Job -Name "m0load_$_" -ScriptBlock {
      $buf = New-Object 'double[]' (150MB / 8)   # ~150 MB touched
      $i = 0L; $acc = 0.0
      while ($true) {
        for ($k = 0; $k -lt 200000; $k++) { $acc += [math]::Sqrt(($k * 1.000173) + $acc) }
        $buf[($i++ % $buf.Length)] = $acc
        if ($i % 64 -eq 0) { $acc = $acc % 100000 }
      }
    } | Out-Null
  }
  Start-Sleep -Seconds 3   # let it spin up
}
function Stop-HostLoad {
  Get-Job -Name 'm0load_*' -ErrorAction SilentlyContinue | Remove-Job -Force
  Write-Host "   synthetic host load stopped"
}

# ---------------------------------------------------------------- concurrent
if (-not $SkipConcurrent) {
  Write-Host "== concurrent_delta pass"
  # ensure resident + warm
  Invoke-Gen (Get-Prompt $Fill ([guid]::NewGuid().ToString('N').Substring(0,8))) $Fill | Out-Null

  foreach ($cond in @('idle','concurrent')) {
    if ($cond -eq 'concurrent') { Start-HostLoad }
    for ($rep = 1; $rep -le $Reps; $rep++) {
      $nonce = [guid]::NewGuid().ToString('N').Substring(0,8)
      try {
        $r = Invoke-Gen (Get-Prompt $Fill $nonce) $Fill
        $md = Metrics-From $r
        $res = Get-Resident
        $rec = [ordered]@{
          schema='m0-concurrent/1'; runtime='ollama'; runtime_version=$ollamaVersion
          model=$ModelTag; quant=$Quant; context_fill=$Fill; condition=$cond; repetition=$rep
          host_load = $(if ($cond -eq 'concurrent') { "synthetic: $($env:NUMBER_OF_PROCESSORS) cpu workers + ~150MB/worker" } else { 'none' })
          timestamp=(Get-Date).ToString('o'); host_ref=$hostRef
          metrics=$md; vram_resident_mb=$res.size_vram_mb
          status='ok'; note='concurrent_delta; host load is a synthetic proxy for editor+LSP+build'
        }
        Save-Record $rec ("concurrent__{0}__{1}__{2}__{3}.json" -f (Slug $ModelTag), $Quant, $cond, $rep)
        Write-Host ("   {0,-10} rep {1}  gen={2} tok/s  prefill={3} tok/s" -f $cond, $rep, $md.gen_tok_s, $md.prefill_tok_s)
      } catch {
        Write-Warning ("   {0} rep {1} -> {2}" -f $cond, $rep, $_)
      }
    }
    if ($cond -eq 'concurrent') { Stop-HostLoad }
  }
}

# ---------------------------------------------------------------- drift
if (-not $SkipDrift) {
  Write-Host ("== sustained_drift pass ({0} min continuous)" -f $DriftMinutes)
  Invoke-Gen (Get-Prompt $Fill ([guid]::NewGuid().ToString('N').Substring(0,8))) $Fill | Out-Null
  $start = Get-Date
  $deadline = $start.AddMinutes($DriftMinutes)
  $i = 0
  while ((Get-Date) -lt $deadline) {
    $i++
    $nonce = [guid]::NewGuid().ToString('N').Substring(0,8)
    $elapsed = [math]::Round(((Get-Date) - $start).TotalSeconds)
    try {
      $r = Invoke-Gen (Get-Prompt $Fill $nonce) $Fill
      $md = Metrics-From $r
      $rec = [ordered]@{
        schema='m0-drift/1'; runtime='ollama'; runtime_version=$ollamaVersion
        model=$ModelTag; quant=$Quant; context_fill=$Fill; iteration=$i
        elapsed_s=$elapsed; timestamp=(Get-Date).ToString('o'); host_ref=$hostRef
        metrics=$md; status='ok'; note='sustained_drift continuous generation'
      }
      Save-Record $rec ("drift__{0}__{1}__{2:d4}.json" -f (Slug $ModelTag), $Quant, $i)
      if ($i % 5 -eq 1) { Write-Host ("   t+{0,4}s  iter {1,3}  gen={2} tok/s" -f $elapsed, $i, $md.gen_tok_s) }
    } catch {
      Write-Warning ("   iter {0} (t+{1}s) -> {2}" -f $i, $elapsed, $_)
      Start-Sleep -Seconds 2
    }
  }
  Write-Host ("   {0} iterations over {1} min" -f $i, $DriftMinutes)
}

Write-Host ""
Write-Host "Done. Records in: $runsDir"
Write-Host "Next: pwsh harness/aggregate.ps1"
