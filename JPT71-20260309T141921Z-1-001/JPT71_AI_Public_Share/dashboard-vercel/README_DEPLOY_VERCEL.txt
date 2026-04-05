JPT71 Dashboard Vercel Deployment Notes

배포 루트
- 이 폴더 자체를 Vercel Root Directory 로 사용합니다.

필수 환경변수
- `JPT71_AI_ENDPOINT=https://api.<your-domain>/api/ai/chat`
- `JPT71_AI_PROXY_TOKEN=<strong-shared-secret>`

왜 runtime inject 인가
- `JPT71_Voyage_Command_Center_Merged.html` 는 `./jpt71-runtime-config.js` 를 먼저 로드합니다.
- `vercel.json` 이 이 요청을 `api/runtime-config.js` 로 rewrite 합니다.
- 따라서 endpoint 와 token 은 Vercel env 에서 런타임 주입되고, HTML 본문에는 하드코딩되지 않습니다.
- 이 경로는 rewrite 가 처리해야 하므로 `dashboard-vercel\jpt71-runtime-config.js` 같은 정적 파일을 따로 두면 안 됩니다.

배포 후 확인
- 공유 URL 은 `https://<your-vercel-project>.vercel.app/`
- 루트는 `index.html` 에서 `JPT71_Voyage_Command_Center_Merged.html` 로 이동합니다.
- 직접 URL 도 유효합니다.
  - `https://<your-vercel-project>.vercel.app/JPT71_Voyage_Command_Center_Merged.html`

변경 시 주의
- 프록시 도메인이 바뀌면 `JPT71_AI_ENDPOINT` 를 갱신합니다.
- 대시보드 도메인이 바뀌면 프록시의 `MYAGENT_PROXY_CORS_ORIGINS` 도 함께 갱신합니다.
