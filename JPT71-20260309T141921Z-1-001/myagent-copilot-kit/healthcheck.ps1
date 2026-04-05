param(
  [string]$BaseUrl = "http://127.0.0.1:3010",
  [string]$Origin = "http://127.0.0.1:4173",
  [string]$ProxyToken = ""
)

$ErrorActionPreference = "Stop"

function Get-StatusCode($scriptBlock) {
  try {
    $resp = & $scriptBlock
    return $resp.StatusCode
  }
  catch {
    if ($_.Exception.Response -and $_.Exception.Response.StatusCode) {
      return $_.Exception.Response.StatusCode.value__
    }
    throw
  }
}

$healthUrl = "$BaseUrl/api/ai/health"
$chatUrl = "$BaseUrl/api/ai/chat"
$headers = @{
  Origin = $Origin
  "x-request-id" = "hc-$(Get-Date -Format yyyyMMddHHmmss)"
}
if ($ProxyToken) {
  $headers["x-ai-proxy-token"] = $ProxyToken
}

$healthStatus = Get-StatusCode { Invoke-WebRequest -Uri $healthUrl -Method Get -UseBasicParsing }
$preflightStatus = Get-StatusCode {
  Invoke-WebRequest -Uri $chatUrl -Method Options -Headers @{
    Origin = $Origin
    "Access-Control-Request-Method" = "POST"
    "Access-Control-Request-Headers" = "content-type,x-request-id,x-ai-proxy-token"
  } -UseBasicParsing
}
$postStatus = Get-StatusCode {
  Invoke-WebRequest -Uri $chatUrl -Method Post -Headers $headers -ContentType "application/json" -Body '{"model":"github-copilot/gpt-5-mini","sensitivity":"internal","messages":[{"role":"user","content":"healthcheck ping"}]}' -UseBasicParsing
}

Write-Host "health GET   : $healthStatus"
Write-Host "preflight    : $preflightStatus"
Write-Host "chat POST    : $postStatus"
Write-Host ""
Write-Host "참고: public 모드에서 ProxyToken 미입력 시 chat POST는 401이 정상입니다."
