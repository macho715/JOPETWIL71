$ErrorActionPreference = "Stop"

$rootDir = Split-Path -Parent $PSScriptRoot
$runtimeDir = Join-Path $rootDir ".runtime"
$proxyDir = Join-Path $rootDir "ai-proxy"
$dashboardDir = Join-Path $rootDir "dashboard"
$dashboardUrl = "http://127.0.0.1:4173/JPT71_Voyage_Command_Center_Merged.html"
$proxyHealthUrl = "http://127.0.0.1:3010/api/ai/health"
$proxyPidFile = Join-Path $runtimeDir "proxy.pid"
$dashboardPidFile = Join-Path $runtimeDir "dashboard.pid"
$staticServerScript = Join-Path $rootDir "tools\serve-static.cjs"

New-Item -ItemType Directory -Path $runtimeDir -Force | Out-Null

function Write-Step($message) {
  Write-Host "[JPT71] $message" -ForegroundColor Cyan
}

function Test-Command($name) {
  return $null -ne (Get-Command $name -ErrorAction SilentlyContinue)
}

function Test-Url($url) {
  try {
    $response = Invoke-WebRequest -UseBasicParsing $url -TimeoutSec 2
    return $response.StatusCode -ge 200 -and $response.StatusCode -lt 400
  } catch {
    return $false
  }
}

function Wait-ForUrl($url, $timeoutSeconds, $label) {
  $deadline = (Get-Date).AddSeconds($timeoutSeconds)
  while ((Get-Date) -lt $deadline) {
    if (Test-Url $url) {
      return
    }
    Start-Sleep -Seconds 1
  }
  throw "$label did not become ready in time: $url"
}

function Invoke-Pnpm {
  param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
  )

  if (Test-Command "pnpm") {
    & pnpm @Args
  } elseif (Test-Command "corepack") {
    & corepack pnpm @Args
  } else {
    throw "Node.js 22+ is required. Install Node.js first."
  }

  if ($LASTEXITCODE -ne 0) {
    throw "pnpm command failed: $($Args -join ' ')"
  }
}

if (-not (Test-Command "node")) {
  throw "Node.js 22+ is required. Install Node.js first."
}

if (-not (Test-Path (Join-Path $proxyDir "dist\cli.js"))) {
  throw "Missing ai-proxy runtime files. Expected: $proxyDir\dist\cli.js"
}

if (-not (Test-Path $staticServerScript)) {
  throw "Missing static server script: $staticServerScript"
}

if (-not (Test-Path (Join-Path $proxyDir "node_modules\express"))) {
  Write-Step "Installing AI proxy dependencies. First run only."
  Push-Location $proxyDir
  try {
    Invoke-Pnpm install --prod --frozen-lockfile
  } finally {
    Pop-Location
  }
} else {
  Write-Step "AI proxy dependencies already installed."
}

Write-Step "Checking GitHub Copilot login."
Push-Location $proxyDir
try {
  & node dist\cli.js token --json *> $null
  if ($LASTEXITCODE -ne 0) {
    Write-Step "GitHub login required. Approve the device login in the browser."
    & node dist\cli.js login
    if ($LASTEXITCODE -ne 0) {
      throw "GitHub device login failed."
    }
  }
} finally {
  Pop-Location
}

if (-not (Test-Url $proxyHealthUrl)) {
  Write-Step "Starting AI proxy on 127.0.0.1:3010."
  $proxyProcess = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "serve-local.bat" -WorkingDirectory $proxyDir -WindowStyle Minimized -PassThru
  Set-Content -Path $proxyPidFile -Value $proxyProcess.Id -Encoding ascii
  Wait-ForUrl $proxyHealthUrl 30 "AI proxy"
} else {
  Write-Step "AI proxy is already running."
}

if (-not (Test-Url $dashboardUrl)) {
  Write-Step "Starting dashboard local server on 127.0.0.1:4173."
  $dashboardProcess = Start-Process -FilePath "node" -ArgumentList @($staticServerScript, $dashboardDir, "4173") -WindowStyle Minimized -PassThru
  Set-Content -Path $dashboardPidFile -Value $dashboardProcess.Id -Encoding ascii
  Wait-ForUrl $dashboardUrl 15 "Dashboard server"
} else {
  Write-Step "Dashboard server is already running."
}

Write-Step "Opening dashboard in the default browser."
Start-Process $dashboardUrl | Out-Null

Write-Host ""
Write-Host "JPT71 AI dashboard is ready." -ForegroundColor Green
Write-Host "Dashboard: $dashboardUrl"
Write-Host "AI Health:  $proxyHealthUrl"
