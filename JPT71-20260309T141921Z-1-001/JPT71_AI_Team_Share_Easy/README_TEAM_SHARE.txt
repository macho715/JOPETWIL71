JPT71 AI Team Share Pack

가장 쉬운 사용 방법
1. 이 폴더를 통째로 압축 해제합니다.
2. Node.js 22.12.0 이상과 `pnpm` 또는 `corepack pnpm` 사용 가능 상태를 준비합니다.
3. `START_JPT71_AI_DASHBOARD.bat` 를 더블클릭합니다.
4. 첫 실행만 GitHub device login 승인 화면이 뜰 수 있습니다.
5. 잠시 후 브라우저가 자동으로 열리면 바로 사용하면 됩니다.

사용 중지
- `STOP_JPT71_AI_DASHBOARD.bat` 를 더블클릭합니다.

팀원 입장에서 필요한 것
- Node.js 22.12.0 이상
- `pnpm` 또는 `corepack pnpm`
- GitHub Copilot 사용 가능한 계정

자동으로 처리되는 것
- AI 프록시 의존성 설치
- Copilot 로그인 확인
- AI 프록시 시작
- 대시보드 로컬 서버 시작
- 브라우저 열기

직접 열 주소
- Dashboard: http://127.0.0.1:4173/JPT71_Voyage_Command_Center_Merged.html
- AI Health: http://127.0.0.1:3010/api/ai/health

폴더 설명
- `dashboard\` : 팀원이 보는 대시보드 세트
- `ai-proxy\` : 로컬 AI 프록시 최소 실행 패키지
- `tools\` : 시작/중지에 필요한 내부 스크립트

운영 기준
- 이 팩은 빠른 로컬 실행용입니다.
- 표준 QA/DLP/퍼블릭 검증은 `ai-proxy\README.md` 와 `myagent-copilot-kit\docs\07-검증-체크리스트.md` 기준으로 별도 수행해야 합니다.

문제 발생 시
1. `START_JPT71_AI_DASHBOARD.bat` 를 다시 실행합니다.
2. 브라우저에서 AI가 안 되면 `http://127.0.0.1:3010/api/ai/health` 가 열리는지 확인합니다.
3. 그래도 안 되면 Node.js 22.12.0 이상과 `pnpm` 또는 `corepack pnpm` 사용 가능 상태를 확인합니다.
