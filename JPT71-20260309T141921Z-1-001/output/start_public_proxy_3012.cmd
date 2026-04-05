@echo off
set MYAGENT_PROXY_HOST=127.0.0.1
set MYAGENT_PROXY_PORT=3012
set MYAGENT_PROXY_AUTH_TOKEN=paV6c3jkY2r19ZxKydo8fXtRHNQWUFsOCTuPevgSJBLEniMh
set MYAGENT_PROXY_CORS_ORIGINS=https://dashboard-vercel-9njbx4xod-chas-projects-08028e73.vercel.app,https://dashboard-vercel-nja815lkj-chas-projects-08028e73.vercel.app,https://dashboard-vercel-mt00j9wf0-chas-projects-08028e73.vercel.app
set MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT=0
node dist\cli.js serve --host 127.0.0.1 --port 3012
