<#
  M1 step 50 - VS Code + Cline, pointed at local Ollama.

  Cline (next bundle, 4.1.16) stores its config file-based under
  %USERPROFILE%\.cline\data\ (relocatable via CLINE_DATA_DIR). Committed
  templates live in provision/config/cline/. This step installs the extension
  and, when Cline is not yet configured, copies the templates into place.
  See provision/config/cline/README.md and
  docs/PROGRESS/M1-baseline-environment.md finding 1.
#>
[CmdletBinding()]
param([switch] $VerifyOnly)
$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$cfgDir = Join-Path $here '..\config'
$tplDir = Join-Path $cfgDir 'cline'
$fail = $false

# Cline's data dir (next bundle). CLINE_DATA_DIR overrides ~/.cline/data.
$clineDataDir  = if ($env:CLINE_DATA_DIR) { $env:CLINE_DATA_DIR } else { Join-Path $env:USERPROFILE '.cline\data' }
$clineSettingsDir = Join-Path $clineDataDir 'settings'
$providersJson    = Join-Path $clineSettingsDir 'providers.json'
$globalJson       = Join-Path $clineSettingsDir 'global-settings.json'
$globalStateJson  = Join-Path $clineDataDir 'globalState.json'

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
$tpl = @{
  providers   = @{ src = Join-Path $tplDir 'providers.json';      dst = $providersJson }
  global      = @{ src = Join-Path $tplDir 'global-settings.json'; dst = $globalJson }
  globalState = @{ src = Join-Path $tplDir 'globalState.json';     dst = $globalStateJson }
}

function Test-OllamaConfigured {
  if (-not (Test-Path $providersJson)) { return $false }
  try {
    $p = Get-Content $providersJson -Raw | ConvertFrom-Json
    return (($p.providers.PSObject.Properties.Name) -contains 'ollama')
  } catch { return $false }
}

if (Test-OllamaConfigured) {
  Write-Output "PASS Cline configured: $providersJson has an 'ollama' provider"
  try {
    $gs = Get-Content $globalStateJson -Raw | ConvertFrom-Json
    if ($gs.actModeOllamaModelId) { Write-Output ("PASS model: {0}  ctx: {1}  timeout: {2}ms" -f $gs.actModeOllamaModelId, $gs.ollamaApiOptionsCtxNum, $gs.requestTimeoutMs) }
    if ($gs.autoApprovalSettings.enabled) { Write-Output "WARN Cline auto-approval is ENABLED - the baseline wants a human to approve every run (see config/cline/README.md)" }
    else { Write-Output "PASS auto-approval disabled" }
    if ($gs.telemetrySetting -and $gs.telemetrySetting -ne 'disabled') { Write-Output "WARN Cline telemetry is '$($gs.telemetrySetting)' - baseline expects 'disabled'" }
  } catch {}
}
elseif ((Test-Path $tpl.providers.src) -and (Test-Path $tpl.globalState.src)) {
  if ($VerifyOnly) {
    Write-Output "FAIL Cline not configured. templates ready at provision/config/cline/ -> $clineDataDir (run without -VerifyOnly, with VS Code closed)"
    $fail = $true
  } else {
    # Refuse to write under a live VS Code - Cline would overwrite on next save.
    $codeRunning = @(Get-Process -Name 'Code','Code - Insiders' -ErrorAction SilentlyContinue).Count -gt 0
    if ($codeRunning) {
      Write-Output "FAIL VS Code is running. Close it and re-run: provision.ps1 -Only 50-editor-cline"
      $fail = $true
    } else {
      New-Item -ItemType Directory -Path $clineSettingsDir -Force | Out-Null
      Copy-Item $tpl.providers.src   $tpl.providers.dst   -Force
      Copy-Item $tpl.global.src      $tpl.global.dst      -Force
      Copy-Item $tpl.globalState.src $tpl.globalState.dst -Force
      Write-Output "DID  copied provision/config/cline/{providers,global-settings,globalState}.json -> $clineDataDir"
      Write-Output "     verify by opening Cline; if it rejects them, reconfigure via the UI and re-capture per config/cline/README.md"
    }
  }
}
else {
  Write-Output "WARN Cline not configured and no template committed. One-time (VS Code):"
  Write-Output "     Cline Settings -> provider Ollama, base URL http://localhost:11434,"
  Write-Output "     model qwen2.5-coder:7b-instruct-q4_K_M, context 16384, timeout 60000, auto-approve OFF, telemetry OFF."
  Write-Output "     Then copy $clineDataDir\settings\providers.json, ...\settings\global-settings.json and"
  Write-Output "     $globalStateJson into provision/config/cline/, curate per that dir's README, and commit."
}

if ($fail) { exit 1 }
exit 0
