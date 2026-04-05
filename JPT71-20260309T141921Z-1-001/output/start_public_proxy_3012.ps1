$env:MYAGENT_PROXY_HOST = "127.0.0.1"
$env:MYAGENT_PROXY_PORT = "3012"
$env:MYAGENT_PROXY_AUTH_TOKEN = "paV6c3jkY2r19ZxKydo8fXtRHNQWUFsOCTuPevgSJBLEniMh"
$env:MYAGENT_PROXY_CORS_ORIGINS = "https://dashboard-vercel-pi.vercel.app,https://dashboard-vercel-chas-projects-08028e73.vercel.app,https://dashboard-vercel-mscho715-9387-chas-projects-08028e73.vercel.app,https://dashboard-vercel-8u1i2a6ze-chas-projects-08028e73.vercel.app"
$env:MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT = "0"

node dist/cli.js serve --host 127.0.0.1 --port 3012
