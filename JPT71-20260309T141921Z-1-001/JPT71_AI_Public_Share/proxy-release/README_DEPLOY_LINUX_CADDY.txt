JPT71 Proxy Deployment Notes

목표
- standalone proxy 를 Linux 서버에서 `127.0.0.1:3010` 또는 `0.0.0.0:3010` 으로 실행
- Caddy 가 `https://api.<your-domain>` 를 받아 proxy 로 전달

필수 조건
- Node.js 22.12.0 이상
- `pnpm`
- 외부에서 접근 가능한 Linux 서버
- DNS 에서 `api.<your-domain>` 가 이 서버를 가리킴

권장 디렉터리 예시
- `/opt/jpt71-ai-proxy`

배포 절차
1. zip 업로드
2. 압축 해제
3. `pnpm install --frozen-lockfile`
4. `pnpm build`
5. `pnpm login`
6. env 설정
7. `systemd` 등록
8. Caddy reload

기준 env
- `MYAGENT_PROXY_HOST=0.0.0.0`
- `MYAGENT_PROXY_PORT=3010`
- `MYAGENT_PROXY_AUTH_TOKEN=<strong-shared-secret>`
- `MYAGENT_PROXY_CORS_ORIGINS=https://<your-vercel-project>.vercel.app`
- `MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT=0`

수동 smoke
- `curl http://127.0.0.1:3010/api/ai/health`
- `curl https://api.<your-domain>/api/ai/health`

운영 주의
- `MYAGENT_PROXY_AUTH_TOKEN` 없이 외부 공개 금지
- `MYAGENT_PROXY_CORS_ORIGINS` 는 실제 대시보드 origin 만 허용
- sanitize payload 외부 전송 허용값은 기본 `0`
