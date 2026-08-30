<#
.SYNOPSIS
  M1 - bring this host to the baseline development environment, or verify it.

.DESCRIPTION
  Runs provision/steps/* in order. Each step is idempotent: it verifies the
  component and only acts if something is missing. Steps print one or more
  lines prefixed PASS / DID / WARN / FAIL and exit non-zero on FAIL.

  This orchestrator NEVER hides a failure or a manual step. Its output is the
  evidence for M1's question ("can the baseline be reconstructed without manual
  repair, and where does it break"). A WARN or a required manual action is
  recorded in the run report, not smoothed over.

.PARAMETER Only
  Run just the named step(s), e.g. -Only 30-ollama,40-models.

.PARAMETER VerifyOnly
  Pass -VerifyOnly through to steps: check and report, change nothing.

.PARAMETER FullModelMatrix
  Pass through to 40-models: pull the entire ~32 GB Ollama matrix, not just the
  working defaults.

.NOTES
  Windows PowerShell 5.1. ASCII only. WSL steps are .sh and are invoked through
  wsl.exe by their wrapper or directly here.
#>

[CmdletBinding()]
param(
  [string[]] $Only,
  [switch]   $VerifyOnly,
  [switch]   $FullModelMatrix
)

$ErrorActionPreference = 'Stop'
$here      = $PSScriptRoot
$stepsDir  = Join-Path $here 'steps'
$reportDir = Join-Path $here '..\run-reports'
if (-not (Test-Path $reportDir)) { New-Item -ItemType Directory -Path $reportDir -Force | Out-Null }

$wslDistro = 'Ubuntu-22.04'   # registered name; see manifest.json note

# ordered step list: name -> how to invoke
$steps = @(
  @{ name = '00-wsl';          kind = 'ps1' }
  @{ name = '10-wsl-prereqs';  kind = 'sh'  }
  @{ name = '20-llamacpp';     kind = 'sh'  }
  @{ name = '30-ollama';       kind = 'ps1' }
  @{ name = '40-models';       kind = 'ps1' }
  @{ name = '50-editor-cline'; kind = 'ps1' }
)

if ($Only) { $steps = $steps | Where-Object { $Only -contains $_.name } }

function Invoke-Step($step) {
  $path = Join-Path $stepsDir ($step.name + '.' + $step.kind)
  if (-not (Test-Path $path)) {
    return [pscustomobject]@{ step = $step.name; status = 'MISSING'; exit = $null; output = "no script at $path" }
  }
  Write-Host ""
  Write-Host ("=== {0} ===" -f $step.name) -ForegroundColor Cyan
  $out = New-Object System.Collections.Generic.List[string]
  $exit = 0
  try {
    if ($step.kind -eq 'ps1') {
      $args = @()
      if ($VerifyOnly)       { $args += '-VerifyOnly' }
      if ($FullModelMatrix -and $step.name -eq '40-models') { $args += '-FullModelMatrix' }
      & powershell -NoProfile -ExecutionPolicy Bypass -File $path @args 2>&1 | ForEach-Object {
        $line = "$_"; $out.Add($line); Write-Host "  $line"
      }
      $exit = $LASTEXITCODE
    } else {
      $wslPath = (& wsl.exe -d $wslDistro wslpath ("'" + $path + "'")).Trim()
      $envPrefix = ''
      if ($VerifyOnly) { $envPrefix = 'VERIFY_ONLY=1 ' }
      & wsl.exe -d $wslDistro -- bash -lc ($envPrefix + "bash '$wslPath'") 2>&1 | ForEach-Object {
        $line = "$_"; $out.Add($line); Write-Host "  $line"
      }
      $exit = $LASTEXITCODE
    }
  } catch {
    $out.Add("orchestrator exception: $_"); $exit = 1
  }
  $status = if ($exit -eq 0) { 'OK' } else { 'FAIL' }
  if (($out -join "`n") -match '(?m)^\s*WARN') { if ($status -eq 'OK') { $status = 'OK_WITH_WARN' } }
  [pscustomobject]@{ step = $step.name; status = $status; exit = $exit; output = ($out -join "`n") }
}

$results = @()
foreach ($s in $steps) {
  $r = Invoke-Step $s
  $results += $r
  if ($r.status -eq 'FAIL') {
    Write-Host ("STOP: {0} failed (exit {1}). Fix and re-run with -Only {0}" -f $r.step, $r.exit) -ForegroundColor Red
    break
  }
}

$stamp  = Get-Date -Format 'yyyyMMdd-HHmmss'
$report = [ordered]@{
  schema     = 'm1-provision-run/0'
  timestamp  = (Get-Date).ToString('o')
  host       = $env:COMPUTERNAME
  verify_only = [bool]$VerifyOnly
  full_matrix = [bool]$FullModelMatrix
  steps      = $results
  overall    = if ($results.status -contains 'FAIL') { 'FAIL' }
               elseif ($results.status -contains 'OK_WITH_WARN') { 'OK_WITH_WARN' }
               elseif ($results.status -contains 'MISSING') { 'INCOMPLETE' }
               else { 'OK' }
}
$reportFile = Join-Path $reportDir "provision-$stamp.json"
$report | ConvertTo-Json -Depth 6 | Set-Content -Path $reportFile -Encoding utf8

Write-Host ""
Write-Host ("overall: {0}   report: {1}" -f $report.overall, $reportFile) -ForegroundColor $(if ($report.overall -like 'OK*') { 'Green' } else { 'Yellow' })
# FAIL / INCOMPLETE are non-zero; OK and OK_WITH_WARN (a documented manual step
# remains, nothing is broken) are success.
if ($report.overall -notlike 'OK*') { exit 1 }
