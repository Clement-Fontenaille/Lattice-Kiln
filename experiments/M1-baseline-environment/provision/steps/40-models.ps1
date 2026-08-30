<#
  M1 step 40 - model assets.
  Default: ensure the working-default Ollama models only (3B Q4, 7B Q4, 7B Q5).
  -FullModelMatrix: pull the entire models.json matrix (~32 GB).
  GGUFs for llama.cpp are handled by step 20.
#>
[CmdletBinding()]
param([switch] $VerifyOnly, [switch] $FullModelMatrix)
$ErrorActionPreference = 'Stop'
$endpoint = 'http://localhost:11434'
$here = $PSScriptRoot
$modelsJson = Join-Path $here '..\..\..\M0-inference-envelope\harness\models.json'
$installDir = Join-Path $env:LOCALAPPDATA 'Programs\Ollama'
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
  if (Test-Path (Join-Path $installDir 'ollama.exe')) { $env:Path = "$installDir;$env:Path" }
}
$fail = $false

$defaults = @(
  'qwen2.5-coder:3b-instruct-q4_K_M',
  'qwen2.5-coder:7b-instruct-q4_K_M',
  'qwen2.5-coder:7b-instruct-q5_K_M'
)

$wanted = $defaults
if ($FullModelMatrix) {
  $cfg = Get-Content $modelsJson -Raw | ConvertFrom-Json
  $wanted = @()
  foreach ($m in $cfg.models) { foreach ($p in $m.ollama.PSObject.Properties) { $wanted += [string]$p.Value } }
  $wanted = $wanted | Sort-Object -Unique
  Write-Output ("full matrix: {0} tags (~32 GB)" -f $wanted.Count)
}

$installed = @()
try { $installed = (Invoke-RestMethod "$endpoint/api/tags").models | ForEach-Object { $_.name } } catch {
  Write-Output "FAIL cannot reach Ollama at $endpoint - run step 30 first."
  exit 1
}

foreach ($tag in $wanted) {
  if ($installed -contains $tag) { Write-Output "PASS have $tag"; continue }
  if ($VerifyOnly) { Write-Output "FAIL missing $tag (verify-only). run: ollama pull $tag"; $fail = $true; continue }
  Write-Output "DID  ollama pull $tag"
  $prev = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
  try { & ollama pull $tag 2>&1 | ForEach-Object { Write-Output "     $_" }; $code = $LASTEXITCODE }
  finally { $ErrorActionPreference = $prev }
  if ($code -ne 0) { Write-Output "FAIL ollama pull $tag exited $code"; $fail = $true }
}

if ($fail) { exit 1 }
Write-Output ("DID  model assets present ({0} tag(s))" -f $wanted.Count)
exit 0
