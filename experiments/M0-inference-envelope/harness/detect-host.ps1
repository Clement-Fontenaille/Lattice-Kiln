<#
.SYNOPSIS
  M0 task 1 - inventory the host for the inference-envelope measurements.

.DESCRIPTION
  Captures CPU, RAM, GPU(s) + VRAM, disk headroom, OS build, WSL layout, and
  which inference runtimes are already present. Writes results/host.json and
  prints a human summary.

  Read-only. Safe to run repeatedly.

.NOTES
  Windows PowerShell 5.1 compatible. Missing pieces are recorded as null, not
  errors - run it even if Ollama / llama.cpp / nvidia-smi are not installed yet.
#>

[CmdletBinding()]
param(
  [string] $OutFile = (Join-Path $PSScriptRoot '..\results\host.json')
)

$ErrorActionPreference = 'Stop'

function Try-Get([scriptblock] $Block) {
  try { & $Block } catch { $null }
}

$host_info = [ordered]@{
  schema     = 'm0-host/1'
  collected  = (Get-Date).ToString('o')
  hostname   = $env:COMPUTERNAME
}

# --- OS ---
$os = Try-Get { Get-CimInstance Win32_OperatingSystem }
$host_info.os = [ordered]@{
  caption = $os.Caption
  version = $os.Version
  build   = $os.BuildNumber
}

# --- CPU ---
$cpu = Try-Get { Get-CimInstance Win32_Processor | Select-Object -First 1 }
$host_info.cpu = [ordered]@{
  name           = $cpu.Name
  cores          = $cpu.NumberOfCores
  logical        = $cpu.NumberOfLogicalProcessors
  max_clock_mhz  = $cpu.MaxClockSpeed
}

# --- RAM ---
$ram_bytes = Try-Get { (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory }
$host_info.ram_gb = if ($ram_bytes) { [math]::Round($ram_bytes / 1GB, 1) } else { $null }

# --- GPU ---
# Win32_VideoController.AdapterRAM is a 32-bit field and wrong above 4 GB.
# Prefer nvidia-smi when present; keep the CIM view as a fallback label.
$gpus = @()
$nvsmi = Try-Get { Get-Command nvidia-smi -ErrorAction Stop }
if ($nvsmi) {
  $raw = Try-Get {
    & nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader,nounits
  }
  foreach ($line in ($raw | Where-Object { $_ -and $_.Trim() })) {
    $p = $line.Split(',') | ForEach-Object { $_.Trim() }
    $gpus += [ordered]@{
      source          = 'nvidia-smi'
      name            = $p[0]
      vram_mb         = [int] $p[1]
      driver_version  = $p[2]
    }
  }
}
if (-not $gpus) {
  $vc = Try-Get { Get-CimInstance Win32_VideoController }
  foreach ($v in $vc) {
    $gpus += [ordered]@{
      source           = 'win32_videocontroller'
      name             = $v.Name
      vram_mb          = if ($v.AdapterRAM -gt 0) { [math]::Round($v.AdapterRAM / 1MB) } else { $null }
      vram_unreliable  = $true
      driver_version   = $v.DriverVersion
    }
  }
}
$host_info.gpus = $gpus

# --- CUDA toolkit (optional) ---
$nvcc = Try-Get { Get-Command nvcc -ErrorAction Stop }
$host_info.cuda_toolkit = if ($nvcc) {
  (Try-Get { (& nvcc --version) -match 'release' } | Select-Object -First 1)
} else { $null }

# --- Disk headroom on the repo drive ---
$drive = (Get-Item $PSScriptRoot).PSDrive.Name
$dsk = Try-Get { Get-PSDrive -Name $drive }
$host_info.disk = [ordered]@{
  drive        = $drive
  free_gb      = if ($dsk) { [math]::Round($dsk.Free / 1GB, 1) } else { $null }
  used_gb      = if ($dsk) { [math]::Round($dsk.Used / 1GB, 1) } else { $null }
}

# --- WSL ---
$wsl = Try-Get { & wsl.exe -l -v 2>$null }
$host_info.wsl = [ordered]@{
  present   = [bool] $wsl
  raw       = if ($wsl) { (($wsl -join "`n") -replace "`0", '').Trim() } else { $null }
}

# --- Inference runtimes already present ---
function Probe-Cmd([string] $Name, [string] $VersionArg) {
  $c = Try-Get { Get-Command $Name -ErrorAction Stop }
  if (-not $c) { return [ordered]@{ present = $false } }
  [ordered]@{
    present = $true
    path    = $c.Source
    version = (Try-Get { (& $Name $VersionArg 2>$null) -join ' ' })
  }
}
$host_info.runtimes = [ordered]@{
  ollama      = Probe-Cmd 'ollama' '--version'
  llama_cli   = Probe-Cmd 'llama-cli' '--version'
  llama_bench = Probe-Cmd 'llama-bench' '--help'
}

# --- Write ---
$dir = Split-Path -Parent $OutFile
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
$json = $host_info | ConvertTo-Json -Depth 6
Set-Content -Path $OutFile -Value $json -Encoding utf8
$resolved = (Resolve-Path $OutFile).Path

# --- Summary ---
Write-Host ""
Write-Host "Host inventory written to: $resolved"
Write-Host "-------------------------------------------"
Write-Host ("OS      : {0} (build {1})" -f $host_info.os.caption, $host_info.os.build)
Write-Host ("CPU     : {0}  ({1}c / {2}t)" -f $host_info.cpu.name, $host_info.cpu.cores, $host_info.cpu.logical)
Write-Host ("RAM     : {0} GB" -f $host_info.ram_gb)
foreach ($g in $host_info.gpus) {
  $vr = if ($g.vram_mb) { "$([math]::Round($g.vram_mb/1024,1)) GB" } else { "unknown" }
  $flag = if ($g.vram_unreliable) { "  (VRAM figure unreliable - install nvidia-smi)" } else { "" }
  Write-Host ("GPU     : {0}  [{1}]  {2}{3}" -f $g.name, $vr, $g.source, $flag)
}
Write-Host ("Disk    : {0}: {1} GB free" -f $host_info.disk.drive, $host_info.disk.free_gb)
Write-Host ("WSL     : {0}" -f $(if ($host_info.wsl.present) { "present" } else { "not detected" }))
Write-Host ("Ollama  : {0}" -f $(if ($host_info.runtimes.ollama.present) { $host_info.runtimes.ollama.version } else { "not installed" }))
Write-Host ("llama.cpp: {0}" -f $(if ($host_info.runtimes.llama_bench.present) { "present" } else { "not installed" }))
Write-Host "-------------------------------------------"
Write-Host "Next: paste results/host.json back, or share GPU + VRAM / RAM / WSL-vs-native so the model matrix can be pinned."
Write-Host ""
