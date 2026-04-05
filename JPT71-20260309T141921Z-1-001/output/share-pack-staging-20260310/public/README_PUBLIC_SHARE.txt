JPT71 AI Public Share Pack

이 패키지는 `Vercel 정적 대시보드 + 별도 HTTPS AI 프록시` 운영용입니다.
로컬 실행 팩이 아니라, 팀원에게 URL 하나를 공유하는 형태로 배포할 때 사용합니다.

구성
- `dashboard-vercel\` : Vercel에 바로 올릴 정적 대시보드 세트
- `proxy-release\` : 공용 HTTPS 프록시에 올릴 standalone release zip과 env 예시
- `CHECKLIST_PUBLIC_QA.txt` : 퍼블릭 오픈 전 확인 항목

1. 대시보드 배포
1. `dashboard-vercel\` 폴더를 Vercel 프로젝트 루트로 사용합니다.
2. Vercel 환경변수에 아래 값을 넣습니다.
   - `JPT71_AI_ENDPOINT=https://api.your-domain.com/api/ai/chat`
   - `JPT71_AI_PROXY_TOKEN=<strong-shared-secret>`
3. 배포 후 공유 링크는 Vercel URL 또는 연결한 커스텀 도메인 하나로 통일합니다.

2. 프록시 배포
1. `proxy-release\myagent-copilot-standalone-v0.1.0.zip` 를 서버에 복사해 압축 해제합니다.
2. 서버 조건은 Node.js 22.12.0 이상, `pnpm`, HTTPS reverse proxy입니다.
3. 아래 env를 기준으로 실행합니다.
   - `MYAGENT_PROXY_HOST=0.0.0.0`
   - `MYAGENT_PROXY_PORT=3010`
   - `MYAGENT_PROXY_AUTH_TOKEN=<strong-shared-secret>`
   - `MYAGENT_PROXY_CORS_ORIGINS=https://<your-vercel-domain>,https://<your-custom-dashboard-domain>`
   - `MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT=0`
4. 실행 절차는 release 압축 해제 후 `pnpm install --frozen-lockfile`, `pnpm build`, `node dist/cli.js serve --host 0.0.0.0 --port 3010` 입니다.

3. 런타임 주입 방식
- 대시보드는 `jpt71-runtime-config.js` 를 먼저 로드합니다.
- Vercel에서는 이 경로를 `api/runtime-config.js` 로 rewrite 해서 env 값을 런타임에 브라우저로 내려줍니다.
- repo 안 HTML에는 프록시 토큰이 하드코딩되어 있지 않습니다.

4. 주의
- 이 구조는 브라우저가 공유 토큰을 직접 보내는 최소 보안안입니다.
- 더 강한 보안이 필요하면 후속 단계에서 BFF 또는 short-lived token 구조로 바꿔야 합니다.
- `MYAGENT_PROXY_AUTH_TOKEN` 과 `MYAGENT_PROXY_CORS_ORIGINS` 없이 외부 공개 운영을 시작하면 안 됩니다.
