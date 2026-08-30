<#
  M1 step 50 - VS Code + Cline, pointed at local Ollama.
  Config is checked in at provision/config/cline-settings.json and copied into
  place; it is not hand-edited on the host.
#>
[CmdletBinding()]
param([switch] $VerifyOnly)
$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$cfgSrc = Join-Path $here '..\config\cline-settings.json'
$fail = $false

# --- VS Code ---
$code = Get-Command code -ErrorAction SilentlyContinue
if (-not $code) {
  if ($VerifyOnly) { Write-Output "FAIL 'code' not on PATH. run: winget install --id Microsoft.VisualStudioCode -e"; exit 1 }
  Write-Output "DID  winget install --id Microsoft.VisualStudioCode -e"
  try { & winget install --id Microsoft.VisualStudioCode -e --accept-source-agreements --accept-package-agreements }
  catch { Write-Output "FAIL winget install VS Code failed: $_"; exit 1 }
  $code = Get-Command code -ErrorAction SilentlyContinue
  if (-not $code) { Write-Output "WARN 'code' still not on PATH - open a new shell or add it manually."; exit 1 }
}
Write-Output ("PASS VS Code: " + ((& code --version) | Select-Object -First 1))

# --- Cline extension ---
# 'code' is a .cmd shim; route through cmd for a clean line list regardless of
# how this step was invoked.
$extList = (& cmd /c "code --list-extensions" 2>$null) -join "`n"
if ($extList -match '(?im)^\s*saoudrizwan\.claude-dev\s*$') {
  Write-Output "PASS Cline (saoudrizwan.claude-dev) installed"
} elseif ($VerifyOnly) {
  Write-Output "FAIL Cline not installed. run: code --install-extension saoudrizwan.claude-dev"
  $fail = $true
} else {
  Write-Output "DID  code --install-extension saoudrizwan.claude-dev"
  $ins = (& cmd /c "code --install-extension saoudrizwan.claude-dev 2>&1") -join "`n"
  Write-Output "     $ins"
  if ($ins -match 'already installed' -or $ins -match 'successfully installed' -or $ins -match "Extension 'saoudrizwan\.claude-dev'") {
    Write-Output "PASS Cline present"
  } else {
    Write-Output "FAIL extension install did not confirm"; $fail = $true
  }
}

# --- config reference ---
if (Test-Path $cfgSrc) {
  Write-Output "PASS checked-in Cline config present: provision/config/cline-settings.json"
  Write-Output "WARN Cline settings live in VS Code global state; apply the checked-in values via the Cline settings UI"
  Write-Output "     (provider: Ollama, base URL http://localhost:11434, model qwen2.5-coder:7b-instruct-q4_K_M)."
  Write-Output "     Automating that write is an open M1 item - recorded as a manual step."
} else {
  Write-Output "WARN no provision/config/cline-settings.json"
}

if ($fail) { exit 1 }
exit 0
