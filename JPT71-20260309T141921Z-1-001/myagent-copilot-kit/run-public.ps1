param(
  [string]$OpenClawHome = ""
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $OpenClawHome) {
  $OpenClawHome = (Resolve-Path (Join-Path $scriptDir "..\..")).Path
}

if (-not (Test-Path (Join-Path $OpenClawHome "package.json"))) {
  throw "package.json not found. Set -OpenClawHome to OpenClaw repo root."
}

if (-not $env:MYAGENT_PROXY_CORS_ORIGINS) {
  throw "MYAGENT_PROXY_CORS_ORIGINS is required in public mode."
}
if (-not $env:MYAGENT_PROXY_AUTH_TOKEN) {
  throw "MYAGENT_PROXY_AUTH_TOKEN is required in public mode."
}

if (-not $env:MYAGENT_PROXY_HOST) { $env:MYAGENT_PROXY_HOST = "0.0.0.0" }
if (-not $env:MYAGENT_PROXY_PORT) { $env:MYAGENT_PROXY_PORT = "3010" }
if (-not $env:MYAGENT_PROXY_OPS_LOGS) { $env:MYAGENT_PROXY_OPS_LOGS = "1" }
if (-not $env:MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT) {
  $env:MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT = "0"
}

Write-Host "OpenClaw root: $OpenClawHome"
Write-Host "Proxy mode: public"
Write-Host "Host/Port : $($env:MYAGENT_PROXY_HOST):$($env:MYAGENT_PROXY_PORT)"
Write-Host "Origins   : $($env:MYAGENT_PROXY_CORS_ORIGINS)"

Push-Location $OpenClawHome
try {
  pnpm myagent:proxy
}
finally {
  Pop-Location
}
