<#
.SYNOPSIS
  M0 - model-switch cost across the Q4_K_M chain (3B -> 7B -> 14B -> 3B).

.DESCRIPTION
  Extracted from bench-ollama.ps1 so switch cost can be measured on its own after
  a staged / interrupted matrix run. switch_ms = unload of the outgoing model +
  cold load of the incoming one, measured as an adjacent pair. Writes m0-switch/1
  records to results/runs/.

.NOTES
  Windows PowerShell 5.1. ASCII only. Requires Ollama running and every tag in
  -Chain already pulled.
#>

[CmdletBinding()]
param(
  [string]   $OutDir    = (Join-Path $PSScriptRoot '..\results'),
  [string]   $ServerUrl = 'http://localhost:11434',
  [string[]] $Chain = @(
    'qwen2.5-coder:3b-instruct-q4_K_M',
    'qwen2.5-coder:7b-instruct-q4_K_M',
    'qwen2.5-coder:14b-instruct-q4_K_M'
  )
)

$ErrorActionPreference = 'Stop'
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
  $od = Join-Path $env:LOCALAPPDATA 'Programs\Ollama'
  if (Test-Path (Join-Path $od 'ollama.exe')) { $env:Path = "$od;$env:Path" }
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

$installed = (Invoke-RestMethod "$ServerUrl/api/tags").models | ForEach-Object { $_.name }
foreach ($t in $Chain) { if ($installed -notcontains $t) { throw "tag not installed: $t" } }

function Unload([string] $Model) {
  $sw = [System.Diagnostics.Stopwatch]::StartNew()
  $body = @{ model = $Model; prompt = ''; stream = $false; keep_alive = 0 } | ConvertTo-Json
  try { Invoke-RestMethod "$ServerUrl/api/generate" -Method Post -Body $body -ContentType 'application/json' -TimeoutSec 60 | Out-Null } catch {}
  for ($i = 0; $i -lt 120; $i++) {
    if (-not ((Invoke-RestMethod "$ServerUrl/api/ps").models | Where-Object { $_.name -eq $Model })) { break }
    Start-Sleep -Milliseconds 250
  }
  $sw.Stop(); [int]$sw.ElapsedMilliseconds
}

function LoadOnce([string] $Model) {
  $body = @{
    model = $Model; prompt = 'ready'; stream = $false; keep_alive = '5m'
    options = @{ num_ctx = 1024; num_predict = 1; temperature = 0; seed = 1 }
  } | ConvertTo-Json -Depth 5
  $r = Invoke-RestMethod "$ServerUrl/api/generate" -Method Post -Body $body -ContentType 'application/json' -TimeoutSec 900
  [math]::Round($r.load_duration / 1e6)
}
function Slug([string] $s) { $s -replace '[:/\\]', '-' }

$chain = @($Chain) + @($Chain[0])   # close the loop
Write-Host ("switch chain: {0}" -f ($chain -join ' -> '))
# prime: make sure the first model is the resident one
Unload $chain[0] | Out-Null
LoadOnce $chain[0] | Out-Null

for ($i = 0; $i -lt $chain.Count - 1; $i++) {
  $from = $chain[$i]; $to = $chain[$i + 1]
  try {
    $unloadMs = Unload $from
    $loadMs   = LoadOnce $to
    $rec = [ordered]@{
      schema = 'm0-switch/1'; runtime = 'ollama'; runtime_version = $ollamaVersion
      from = $from; to = $to; unload_ms = $unloadMs; load_ms = $loadMs
      switch_ms = $unloadMs + $loadMs
      timestamp = (Get-Date).ToString('o'); host_ref = $hostRef
      note = 'standalone bench-switch.ps1; load_ms is cold load_duration of the incoming model'
    }
    $rec | ConvertTo-Json -Depth 6 | Set-Content -Path (Join-Path $runsDir ("switch__{0}__to__{1}.json" -f (Slug $from), (Slug $to))) -Encoding utf8
    Write-Host ("  {0,-38} -> {1,-38}  unload={2,5} ms  load={3,6} ms  switch={4,6} ms" -f $from, $to, $unloadMs, $loadMs, $rec.switch_ms)
  } catch {
    Write-Warning "switch $from -> ${to}: $_"
  }
}
Write-Host "Done."
