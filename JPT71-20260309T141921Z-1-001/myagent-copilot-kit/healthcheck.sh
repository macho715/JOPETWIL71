#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://127.0.0.1:3010}"
ORIGIN="${2:-http://127.0.0.1:4173}"
PROXY_TOKEN="${3:-}"
REQUEST_ID="hc-$(date +%Y%m%d%H%M%S)"

health_status="$(curl -sS -o /dev/null -w "%{http_code}" "$BASE_URL/api/ai/health")"
preflight_status="$(curl -sS -o /dev/null -w "%{http_code}" -X OPTIONS "$BASE_URL/api/ai/chat" \
  -H "Origin: $ORIGIN" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type,x-request-id,x-ai-proxy-token")"

if [[ -n "$PROXY_TOKEN" ]]; then
  token_header=(-H "x-ai-proxy-token: $PROXY_TOKEN")
else
  token_header=()
fi

post_status="$(curl -sS -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/api/ai/chat" \
  -H "Origin: $ORIGIN" \
  -H "Content-Type: application/json" \
  -H "x-request-id: $REQUEST_ID" \
  "${token_header[@]}" \
  --data '{"model":"github-copilot/gpt-5-mini","sensitivity":"internal","messages":[{"role":"user","content":"healthcheck ping"}]}')"

echo "health GET   : $health_status"
echo "preflight    : $preflight_status"
echo "chat POST    : $post_status"
echo
echo "참고: public 모드에서 ProxyToken 미입력 시 chat POST는 401이 정상입니다."
