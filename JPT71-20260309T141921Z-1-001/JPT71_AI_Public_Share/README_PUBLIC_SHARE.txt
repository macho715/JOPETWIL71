JPT71 AI Public Share Pack

이 패키지는 `Vercel 정적 대시보드 + 별도 HTTPS AI 프록시` 운영용입니다.
로컬 실행 팩이 아니라, 팀원에게 URL 하나를 공유하는 형태로 배포할 때 사용합니다.

구성
- `dashboard-vercel\` : Vercel에 바로 올릴 정적 대시보드 세트
- `proxy-release\` : 공용 HTTPS 프록시에 올릴 standalone release zip과 env 예시
- `RUNBOOK_PUBLIC_DEPLOYMENT.txt` : 처음부터 끝까지 따라가는 배포 순서
- `HANDOFF_INPUTS_TEMPLATE.txt` : 배포 전에 채워야 하는 사용자 입력값 템플릿
- `CHECKLIST_PUBLIC_QA.txt` : 퍼블릭 오픈 전 확인 항목
- `DEPLOYMENT_VERIFICATION_REPORT_2026-03-10.md` : 실제 구현/배포/검증/한계 사항 상세 기록

가장 먼저 할 일
1. `HANDOFF_INPUTS_TEMPLATE.txt` 를 채웁니다.
2. `RUNBOOK_PUBLIC_DEPLOYMENT.txt` 순서대로 Vercel 과 Linux 서버를 준비합니다.
3. 배포가 끝나면 `CHECKLIST_PUBLIC_QA.txt` 기준으로 검증합니다.

기본 운영안
- 대시보드: `Vercel 기본 도메인` 먼저 사용
- 프록시: `Linux + Caddy` 로 `https://api.<your-domain>` 제공
- 토큰: `runtime inject` 로만 주입
- sanitize 정책: `MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT=0`

초기 공유 URL
- `https://<your-vercel-project>.vercel.app/`
- 또는 `https://<your-vercel-project>.vercel.app/JPT71_Voyage_Command_Center_Merged.html`

주의
- 이 구조는 브라우저가 공유 토큰을 직접 보내는 최소 보안안입니다.
- 더 강한 보안이 필요하면 후속 단계에서 BFF 또는 short-lived token 구조로 바꿔야 합니다.
- `MYAGENT_PROXY_AUTH_TOKEN` 과 `MYAGENT_PROXY_CORS_ORIGINS` 없이 외부 공개 운영을 시작하면 안 됩니다.
