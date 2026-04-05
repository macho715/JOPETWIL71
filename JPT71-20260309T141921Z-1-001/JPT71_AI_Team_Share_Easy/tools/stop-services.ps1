$ErrorActionPreference = "Stop"

$rootDir = Split-Path -Parent $PSScriptRoot
$runtimeDir = Join-Path $rootDir ".runtime"
$pidFiles = @(
  @{ Name = "AI proxy"; Path = Join-Path $runtimeDir "proxy.pid" },
  @{ Name = "Dashboard server"; Path = Join-Path $runtimeDir "dashboard.pid" }
)

function Write-Step($message) {
  Write-Host "[JPT71] $message" -ForegroundColor Cyan
}

$stoppedAny = $false

foreach ($item in $pidFiles) {
  if (-not (Test-Path $item.Path)) {
    continue
  }

  $rawPid = (Get-Content $item.Path -ErrorAction SilentlyContinue | Select-Object -First 1).Trim()
  Remove-Item $item.Path -Force -ErrorAction SilentlyContinue

  if (-not $rawPid) {
    continue
  }

  try {
    $pidValue = [int]$rawPid
  } catch {
    continue
  }

  $process = Get-Process -Id $pidValue -ErrorAction SilentlyContinue
  if ($process) {
    Write-Step "Stopping $($item.Name) (PID $pidValue)."
    Stop-Process -Id $pidValue -Force -ErrorAction Stop
    $stoppedAny = $true
  }
}

if (-not $stoppedAny) {
  Write-Host "No managed JPT71 processes were running." -ForegroundColor Yellow
} else {
  Write-Host "JPT71 local services stopped." -ForegroundColor Green
}
