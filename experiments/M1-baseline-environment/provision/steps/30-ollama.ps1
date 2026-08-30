<#
  M1 step 30 - Ollama (native Windows), runtime of record.
  Verify install + server. Install via winget if missing and not -VerifyOnly.
#>
[CmdletBinding()]
param([switch] $VerifyOnly)
$ErrorActionPreference = 'Stop'
$endpoint = 'http://localhost:11434'
$installDir = Join-Path $env:LOCALAPPDATA 'Programs\Ollama'
$fail = $false

function Resolve-Ollama {
  $c = Get-Command ollama -ErrorAction SilentlyContinue
  if ($c) { return $c.Source }
  $p = Join-Path $installDir 'ollama.exe'
  if (Test-Path $p) { return $p }
  return $null
}

$exe = Resolve-Ollama
if (-not $exe) {
  if ($VerifyOnly) {
    Write-Output "FAIL ollama not installed. run: winget install --id Ollama.Ollama -e"
    exit 1
  }
  Write-Output "DID  winget install --id Ollama.Ollama -e"
  try {
    & winget install --id Ollama.Ollama -e --accept-source-agreements --accept-package-agreements
  } catch {
    Write-Output "FAIL winget install failed: $_"
    Write-Output "     fallback (operator): download the installer from https://ollama.com/download/windows"
    exit 1
  }
  $exe = Resolve-Ollama
  if (-not $exe) { Write-Output "FAIL still not found after install."; exit 1 }
}
Write-Output "PASS ollama.exe at $exe"

$ver = try { (& $exe --version) -join ' ' } catch { 'unknown' }
Write-Output "PASS $ver"
if ($exe -notmatch [regex]::Escape($installDir)) {
  Write-Output "WARN ollama.exe is not under $installDir - harness scripts self-locate that path; update them or PATH."
}

# --- server up ---
$up = $false
for ($i = 0; $i -lt 3; $i++) {
  try { Invoke-RestMethod -Uri "$endpoint/api/tags" -TimeoutSec 5 | Out-Null; $up = $true; break } catch { Start-Sleep 2 }
}
if ($up) {
  Write-Output "PASS server responding at $endpoint"
} elseif ($VerifyOnly) {
  Write-Output "FAIL server not responding at $endpoint (start Ollama)."
  $fail = $true
} else {
  Write-Output "DID  starting ollama serve (background)"
  Start-Process -FilePath $exe -ArgumentList 'serve' -WindowStyle Hidden
  Start-Sleep 4
  try { Invoke-RestMethod -Uri "$endpoint/api/tags" -TimeoutSec 5 | Out-Null; Write-Output "PASS server up after start" }
  catch { Write-Output "FAIL server still not responding after 'ollama serve'"; $fail = $true }
}

if ($fail) { exit 1 }
exit 0
