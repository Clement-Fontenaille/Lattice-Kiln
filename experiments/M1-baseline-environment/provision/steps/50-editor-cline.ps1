<#
  M1 step 50 - VS Code + Cline, pointed at local Ollama.

  Cline stores provider/model config in JSON under its VS Code globalStorage
  (providers.json, global-settings.json). Those files are file-based and thus
  scriptable, but the schema is undocumented and zod-validated on load, and Cline
  is UI-first for configuration (see docs/PROGRESS/M1-baseline-environment.md
  finding 1). So: if committed templates exist under provision/config/, copy them
  into place; otherwise report the exact manual steps as WARN.
#>
[CmdletBinding()]
param([switch] $VerifyOnly)
$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$cfgDir = Join-Path $here '..\config'
$fail = $false

# Cline's VS Code-extension settings dir (empirically confirmed on this host).
$clineSettingsDir = Join-Path $env:APPDATA 'Code\User\globalStorage\saoudrizwan.claude-dev\settings'
$providersJson    = Join-Path $clineSettingsDir 'providers.json'
$globalJson       = Join-Path $clineSettingsDir 'global-settings.json'

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

# --- Cline provider/model config ---
$tplProviders = Join-Path $cfgDir 'providers.json'
$tplGlobal    = Join-Path $cfgDir 'global-settings.json'

if (Test-Path $providersJson) {
  Write-Output "PASS Cline providers.json present: $providersJson"
  $isOllama = $false
  try { $isOllama = ((Get-Content $providersJson -Raw | ConvertFrom-Json).providers.PSObject.Properties.Name) -contains 'ollama' } catch {}
  if ($isOllama) { Write-Output "PASS providers.json has an 'ollama' provider" }
  else { Write-Output "WARN providers.json exists but has no 'ollama' provider - configure it in the Cline UI" }
}
elseif ((Test-Path $tplProviders)) {
  if ($VerifyOnly) {
    Write-Output "FAIL Cline not configured. template available: provision/config/providers.json -> $providersJson"
    $fail = $true
  } else {
    New-Item -ItemType Directory -Path $clineSettingsDir -Force | Out-Null
    Copy-Item $tplProviders $providersJson -Force
    if (Test-Path $tplGlobal) { Copy-Item $tplGlobal $globalJson -Force }
    Write-Output "DID  copied committed Cline templates into $clineSettingsDir"
    Write-Output "WARN templates use Cline's undocumented settings schema; if Cline rejects them, delete and reconfigure via the UI, then re-capture."
  }
}
else {
  Write-Output "WARN Cline is not configured and no template is committed. Manual, one-time:"
  Write-Output "     1. VS Code -> Cline -> Settings: provider = Ollama, base URL = http://localhost:11434,"
  Write-Output "        model = qwen2.5-coder:7b-instruct-q4_K_M, auto-approve = off."
  Write-Output "     2. Copy $providersJson and $globalJson"
  Write-Output "        into provision/config/ and commit them as templates; future provisions copy them."
  Write-Output "     Reference values + rationale: provision/config/cline-settings.json"
  Write-Output "     Empty providers.json shape is { `"version`": 1, `"providers`": {} }."
}

if ($fail) { exit 1 }
exit 0
