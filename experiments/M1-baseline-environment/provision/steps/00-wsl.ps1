<#
  M1 step 00 - WSL2 + distro + GPU passthrough.
  Verify-only capable. Does not install a distro (operator action); reports if
  one is needed.
#>
[CmdletBinding()]
param([switch] $VerifyOnly)
$ErrorActionPreference = 'Stop'
$distro = 'Ubuntu-22.04'   # registered name

$fail = $false

# --- WSL present + version 2 ---
$wslList = try { (& wsl.exe -l -v) -replace "`0", '' } catch { $null }
if (-not $wslList) {
  Write-Output "FAIL wsl.exe not available. Install: wsl --install -d Ubuntu-24.04 (operator, needs reboot)."
  exit 1
}
if ($wslList -match [regex]::Escape($distro)) {
  Write-Output "PASS distro '$distro' registered."
} else {
  Write-Output "FAIL distro '$distro' not found. Registered distros:"
  $wslList | ForEach-Object { if ($_ -match '\S') { Write-Output "     $_" } }
  Write-Output "     Fix: wsl --install -d Ubuntu-24.04 (operator)."
  exit 1
}

# --- default version 2 ---
$defVer = ($wslList | Select-String -Pattern ("\*\s+" + [regex]::Escape($distro) + "\s+\w+\s+(\d)")).Matches.Groups[1].Value
if ($defVer -and $defVer -ne '2') { Write-Output "WARN  $distro is WSL version $defVer, expected 2." }
else { Write-Output "PASS $distro on WSL2." }

# --- GPU passthrough: nvidia-smi inside WSL ---
$smi = try { (& wsl.exe -d $distro -- bash -lc 'nvidia-smi -L 2>&1') } catch { "$_" }
if ("$smi" -match 'GPU 0:') {
  Write-Output ("PASS GPU visible in WSL: " + ("$smi" -split "`n")[0].Trim())
} else {
  Write-Output "FAIL nvidia-smi -L failed inside WSL. Need an NVIDIA Windows driver with WSL GPU support (operator)."
  Write-Output ("     got: " + ("$smi" -replace "`n", ' ').Trim())
  $fail = $true
}

# --- CUDA driver lib present (not the toolkit - that is step 10) ---
$libcuda = try { (& wsl.exe -d $distro -- bash -lc 'ls /usr/lib/wsl/lib/libcuda.so.1 2>&1') } catch { "$_" }
if ("$libcuda" -match 'libcuda.so.1') { Write-Output "PASS /usr/lib/wsl/lib/libcuda.so.1 present." }
else { Write-Output "WARN libcuda.so.1 not found under /usr/lib/wsl/lib - GPU builds may not link." }

if ($fail) { exit 1 }
Write-Output "DID  nothing to change (verify step)."
exit 0
