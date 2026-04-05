param(
  [string]$OpenClawHome = ""
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $OpenClawHome) {
  $OpenClawHome = (Resolve-Path (Join-Path $scriptDir "..\..")).Path
}

if (-not (Test-Path (Join-Path $OpenClawHome "scripts\\myagent-proxy.mjs"))) {
  throw "scripts/myagent-proxy.mjs not found. Set -OpenClawHome to OpenClaw repo root."
}

if (-not $env:MYAGENT_PROXY_HOST) { $env:MYAGENT_PROXY_HOST = "127.0.0.1" }
if (-not $env:MYAGENT_PROXY_PORT) { $env:MYAGENT_PROXY_PORT = "3010" }
if (-not $env:MYAGENT_PROXY_OPS_LOGS) { $env:MYAGENT_PROXY_OPS_LOGS = "1" }
if (-not $env:MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT) {
  $env:MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT = "0"
}

Write-Host "OpenClaw root      : $OpenClawHome"
Write-Host "Execution mode     : standalone-direct"
Write-Host "Proxy mode         : local"
Write-Host "Host/Port          : $($env:MYAGENT_PROXY_HOST):$($env:MYAGENT_PROXY_PORT)"
Write-Host "Launch command     : node --import tsx scripts/myagent-proxy.mjs"

Push-Location $OpenClawHome
try {
  node --import tsx scripts/myagent-proxy.mjs
}
finally {
  Pop-Location
}
