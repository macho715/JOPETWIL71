#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_HOME="${OPENCLAW_HOME:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

if [[ ! -f "$OPENCLAW_HOME/package.json" ]]; then
  echo "package.json not found. Set OPENCLAW_HOME to OpenClaw repo root." >&2
  exit 1
fi

export MYAGENT_PROXY_HOST="${MYAGENT_PROXY_HOST:-127.0.0.1}"
export MYAGENT_PROXY_PORT="${MYAGENT_PROXY_PORT:-3010}"
export MYAGENT_PROXY_OPS_LOGS="${MYAGENT_PROXY_OPS_LOGS:-1}"
export MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT="${MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT:-0}"

echo "OpenClaw root: $OPENCLAW_HOME"
echo "Proxy mode: local"
echo "Host/Port : $MYAGENT_PROXY_HOST:$MYAGENT_PROXY_PORT"

cd "$OPENCLAW_HOME"
pnpm myagent:proxy
