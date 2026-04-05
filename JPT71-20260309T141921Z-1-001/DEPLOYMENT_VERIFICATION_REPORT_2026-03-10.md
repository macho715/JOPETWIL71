# JPT71 AI Dashboard Deployment Verification Report

## 1. 문서 목적

이 문서는 2026-03-10 기준으로 JPT71 Voyage Command Center에 AI 기능을 추가하고, standalone AI proxy를 연결하고, 실제 공개 배포와 검증까지 진행한 결과를 상세히 기록한다.

이 문서의 목적은 아래 4가지다.

- 무엇을 구현했고 무엇을 배포했는지 남긴다.
- README 및 docs 기준과 실제 동작 사이의 차이를 기록한다.
- 실제로 검증된 항목과 아직 남아 있는 제약을 분리해서 남긴다.
- 이후 Linux + Caddy + 실도메인 운영으로 승격할 때 출발점을 남긴다.

이 문서는 운영 요약 문서인 `LIVE_DEPLOYMENT_STATUS_2026-03-10.txt`보다 상세하며, `RUNBOOK_PUBLIC_DEPLOYMENT.txt`보다 현재 상태와 실제 검증 기록에 더 초점을 둔다.

## 2. 현재 상태 한 줄 요약

- 대시보드 AI 기능 구현 완료
- standalone proxy 연동 완료
- `Vercel + ngrok` 기준 실제 공개 동작 확인 완료
- 브라우저에서 실제 preset 호출과 공개 HTTPS endpoint 호출 확인 완료
- 장기 안정 운영용 `Linux + Caddy + 실도메인` 전환은 아직 미완료

## 3. 현재 공개 URL

2026-03-10 기준 현재 공개 URL은 아래와 같다.

- 대시보드 루트: `https://dashboard-vercel-chas-projects-08028e73.vercel.app/`
- 대시보드 직접 경로: `https://dashboard-vercel-chas-projects-08028e73.vercel.app/JPT71_Voyage_Command_Center_Merged.html`
- 공개 AI proxy: `https://07d3-2-50-178-28.ngrok-free.app/api/ai/chat`
- proxy health: `https://07d3-2-50-178-28.ngrok-free.app/api/ai/health`

주의:

- 현재 proxy는 `ngrok free tunnel`에 의존하므로 URL이 고정되지 않을 수 있다.
- 장기 공유 링크는 대시보드 URL 쪽은 유지 가능하지만, proxy URL은 ngrok가 바뀌면 같이 갱신해야 한다.

## 4. 구현 범위

### 4.1 대시보드 AI 패널

대상 파일:

- `DASHBOARD/JPT71_Voyage_Command_Center_Merged.html`

구현 범위:

- `Action Ideas` 탭 내부에 AI 제안 카드 추가
- preset 버튼 추가
- 자유 질문 입력창 추가
- plain text 응답 렌더링
- 로딩/에러 상태 처리
- 기간 변경 후 stale 안내
- runtime config 기반 endpoint/token 주입

### 4.2 추가된 AI preset

초기 preset:

- 원인 요약
- 실행 액션
- 리스크 점검
- Gap 설명

추가 preset:

- 우선순위 랭킹
- 다음 확인 경로
- 경영진 5줄 브리프
- 데이터 신뢰도 점검
- 기간 비교
- 비용 전환 설명

### 4.3 payload 제약

README 및 docs 기준을 반영해 아래 원칙을 지켰다.

- 요약 JSON만 전송
- 전체 `DATA` 미전송
- raw heatmap 배열 미전송
- `monthly_data` 원배열 미전송
- `top15` raw dump 미전송
- 응답은 `innerHTML`이 아니라 plain text로만 표시

## 5. standalone package / docs 기준 확인 결과

### 5.1 맞았던 부분

문서와 실제 구현이 일치하는 부분:

- endpoint는 `POST /api/ai/chat`
- 헤더는 `x-request-id`, `x-ai-sensitivity`, 선택적 `x-ai-proxy-token`
- 대시보드는 요약 JSON만 proxy로 전달
- 응답은 plain text 렌더링
- public 운영에서는 `AUTH_TOKEN`, `CORS_ORIGINS`, HTTPS가 필요

### 5.2 문서와 실제 운영 기본값 차이로 확인된 문제

문서 검토 중 확인된 핵심 이슈는 3가지였다.

1. `MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT`
- 문서 기본 권장값은 `0`
- 실제 로컬/public 실행 스크립트 일부는 기본값이 `1`
- 이 불일치를 모두 `0`으로 수정했다

2. 설치 전제 조건 안내 부족
- 문서는 Node `22.12.0+`와 `pnpm` 또는 `corepack pnpm` 기준
- 쉬운 공유 팩 문구는 `Node.js 22 이상` 정도로 약했다
- 공유 팩 안내와 부트스트랩 스크립트를 문서 기준으로 맞췄다

3. `docs/07` 전체 검증과 쉬운 실행 스크립트를 혼동할 가능성
- 쉬운 실행 스크립트는 편의용
- 문서의 표준 검증 절차는 더 넓다
- 두 개를 분리해서 기록하도록 문서 표현을 보강했다

## 6. 코드 및 패키지 수정 사항

### 6.1 대시보드 쪽

- `DASHBOARD/JPT71_Voyage_Command_Center_Merged.html`
  - AI 패널 추가
  - runtime config 로드
  - ngrok public endpoint 호출 시 `ngrok-skip-browser-warning` 헤더 추가

- `DASHBOARD/jpt71-runtime-config.js`
  - 기본 no-op runtime config 파일 추가
  - 로컬 기본값 fallback 용도

### 6.2 standalone package 쪽

- `myagent-copilot-kit/standalone-package/src/copilot-bridge.ts`
  - Copilot prompt 요청 시 `Editor-Version` 및 `User-Agent` 헤더 추가
  - 실제 Copilot route에서 발생한 `missing Editor-Version header` 오류를 해결

- `myagent-copilot-kit/standalone-package/src/server.ts`
  - CORS 허용 헤더에 `ngrok-skip-browser-warning` 추가

- 실행 스크립트와 env 예시 전반
  - `MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT=0` 기준으로 통일

### 6.3 공유 팩 / 공개 배포 팩

- `JPT71_AI_Team_Share_Easy`
  - Node `22.12.0+` 기준 반영
  - `pnpm/corepack` 전제 조건 반영
  - 로컬 쉬운 실행 문구 보정

- `JPT71_AI_Public_Share`
  - `dashboard-vercel` 추가
  - `proxy-release` 추가
  - handoff/runbook/QA/checklist 문서 추가
  - live deployment status 문서 추가

## 7. 실제 공개 배포 작업 기록

### 7.1 standalone build 및 release 산출물

실행 완료:

- `pnpm install --frozen-lockfile`
- `pnpm build`
- `node export-release.mjs`

결과:

- `myagent-copilot-kit/standalone-package/release/myagent-copilot-standalone-v0.1.0.zip` 생성 완료

### 7.2 Vercel 배포

실제 Vercel 배포를 수행했고, 최종적으로 현재 stable alias로 접근 가능한 상태를 확인했다.

확인된 alias:

- `https://dashboard-vercel-pi.vercel.app`
- `https://dashboard-vercel-chas-projects-08028e73.vercel.app`
- `https://dashboard-vercel-mscho715-9387-chas-projects-08028e73.vercel.app`

운영 기준 공유 URL은 아래로 정리했다.

- `https://dashboard-vercel-chas-projects-08028e73.vercel.app/`

### 7.3 runtime config shadowing 문제와 해결

실제 배포 중 중요한 문제를 한 번 발견했다.

문제:

- `dashboard-vercel/jpt71-runtime-config.js` 정적 파일이 존재하면
- Vercel의 `vercel.json` rewrite가 `api/runtime-config.js`로 가지 않고
- 정적 파일이 그대로 응답된다
- 결과적으로 Vercel env 기반 runtime inject가 동작하지 않는다

영향:

- 공개 대시보드가 runtime endpoint/token을 못 받고
- 로컬 fallback 또는 빈 값으로 동작할 수 있다

조치:

- `JPT71_AI_Public_Share/dashboard-vercel/jpt71-runtime-config.js` 제거
- `README_DEPLOY_VERCEL.txt`에 "이 경로는 rewrite가 처리해야 하므로 정적 파일을 두면 안 된다"는 운영 주의 추가

결과:

- `/jpt71-runtime-config.js` 호출 시 Vercel env가 반영된 JavaScript를 반환하는 것 확인

### 7.4 공개 proxy 구성

현재 공개 proxy는 아래 구조다.

- local standalone proxy: `127.0.0.1:3012`
- ngrok tunnel: `https://07d3-2-50-178-28.ngrok-free.app`

구성 포인트:

- `MYAGENT_PROXY_AUTH_TOKEN` 설정
- `MYAGENT_PROXY_CORS_ORIGINS`에 현재 Vercel alias 추가
- `MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT=0`
- ngrok interstitial 우회를 위해 `ngrok-skip-browser-warning` 헤더 사용

### 7.5 proxy public smoke test

확인 완료:

- `GET http://127.0.0.1:3012/api/ai/health`
- stable alias origin에서 `OPTIONS /api/ai/chat` -> `204`
- public HTTPS endpoint로 `POST /api/ai/chat` -> `200`

즉, proxy 단독 공개 경로는 정상 동작하는 것이 확인되었다.

## 8. 브라우저 검증 결과

Playwright 기반 실제 브라우저 검증을 수행했다.

검증 시나리오:

1. 공개 Vercel URL 열기
2. `Action Ideas` 탭 진입
3. `우선순위 랭킹` preset 클릭
4. AI 응답 대기
5. 응답 수신 확인
6. 네트워크 요청 대상 확인

결과:

- AI 응답 수신 성공
- 응답은 plain text로 표시됨
- 브라우저 네트워크에서 요청 대상이 `127.0.0.1`이 아니라 공개 HTTPS endpoint인 것 확인
- 실제 요청:
  - `POST https://07d3-2-50-178-28.ngrok-free.app/api/ai/chat`
- 응답 상태:
  - `200`

이는 "브라우저에서 실제 공개 URL을 열고, 사용자 동작으로 preset을 눌렀을 때, 공개 proxy가 동작한다"는 것을 의미한다.

## 9. 실제로 확인된 운영 한계

### 9.1 아직 안정 운영이 아닌 이유

현재 구조는 실제 공개 동작까지는 확인했지만, 장기 안정 운영이라고 부르기에는 부족하다.

이유:

- proxy가 현재 내 PC에서 돌아간다
- 내 PC가 꺼지면 proxy도 멈춘다
- ngrok free tunnel URL은 바뀔 수 있다
- 브라우저가 공유 proxy token을 보내는 최소 보안 구조다

즉, 지금 상태는 "내부 검증/데모/파일럿"에는 충분하지만, 장기 고정 운영으로 보기 어렵다.

### 9.2 왜 Linux + Caddy + 실도메인으로 아직 못 갔는가

현재 세션에서 확인한 결과, 아래 정보나 자원이 존재하지 않았다.

- SSH 가능한 외부 Linux 서버
- 실도메인과 DNS 제어 정보
- 클라우드 배포 자격증명

추가 확인 내용:

- `~/.ssh/config`에 있는 유일한 host는 `termux-usb`
- 실제 SSH 연결 시 `Connection refused`

따라서 현재 환경만으로는 Linux + Caddy + 실도메인 배포를 끝까지 진행할 수 없었다.

## 10. 무료 대안 검토 결과

실제 검토한 무료 대안은 아래와 같다.

### 10.1 현재 유지

- `Vercel Hobby + ngrok Free`
- 지금 이미 동작 중인 방식
- 데모/파일럿에는 충분

### 10.2 좀 더 나은 무료 구조

- `Vercel Hobby + Cloudflare Tunnel`
- 내 PC를 계속 쓰되 ngrok 대신 Cloudflare Tunnel 사용
- 도메인이 이미 있으면 무료 인프라 운영에 가장 가까움

### 10.3 제한적 무료 공개

- `Tailscale Funnel`
- 개인/제한된 사용 시 대안 가능
- 다만 회사/팀 운영용으로는 플랜과 약관 확인 필요

### 10.4 조건부 대안

`MYAGENT_GITHUB_TOKEN` 등 환경변수 주입이 가능하므로, 구조적으로는 `pnpm login`이 없는 원격 배포도 가능하다.

확인 근거:

- `README.md`에 `MYAGENT_GITHUB_TOKEN`이 device login 대체 가능하다고 명시
- `src/auth-store.ts`는 `MYAGENT_GITHUB_TOKEN`, `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN` 순서로 env를 직접 확인
- `src/runtime-token.ts`는 그 GitHub token으로 runtime token을 재발급 가능

의미:

- 장기적으로는 PaaS형 호스팅으로도 이식 가능성이 있다
- 다만 이 문서 시점에는 실제로 그 경로까지 배포 실행하지는 않았다

## 11. 산출물

현재 확인 가능한 주요 산출물:

- 공개 배포 킷:
  - `JPT71_AI_Public_Share_2026-03-10_live.zip`
- 공개 배포 팩 폴더:
  - `JPT71_AI_Public_Share/`
- live 상태 요약:
  - `JPT71_AI_Public_Share/LIVE_DEPLOYMENT_STATUS_2026-03-10.txt`
- 배포 런북:
  - `JPT71_AI_Public_Share/RUNBOOK_PUBLIC_DEPLOYMENT.txt`
- Vercel 배포 가이드:
  - `JPT71_AI_Public_Share/dashboard-vercel/README_DEPLOY_VERCEL.txt`

## 12. 비밀정보 취급 원칙

이 문서에는 아래 항목을 기록하지 않는다.

- `MYAGENT_PROXY_AUTH_TOKEN` 실제 값
- GitHub token 실제 값
- runtime token 실제 값

원칙:

- 비밀값은 운영 환경변수 또는 로컬 안전 저장소에만 둔다
- 문서에는 위치와 처리 원칙만 남긴다

## 13. 다음 단계 권장안

우선순위 기준 다음 단계는 아래 순서가 적절하다.

1. 현재 공개 URL로 내부 사용자 테스트 진행
2. 팀 피드백 수집
3. 장기 운영 필요 여부 결정
4. 장기 운영이 필요하면 아래 중 하나 선택
   - Cloudflare Tunnel 기반 무료 운영 고도화
   - Linux + Caddy + 실도메인으로 승격
   - 환경변수 토큰 기반 PaaS 배포 검토

## 14. 결론

2026-03-10 기준으로 확인된 사실은 명확하다.

- JPT71 대시보드 AI 기능은 구현 완료다.
- standalone proxy와의 연동은 동작한다.
- `Vercel + ngrok` 기준 실제 공개 동작도 확인됐다.
- README 및 docs 기준에서 문제였던 보안 기본값과 문서 정합성도 보정했다.
- 다만 현재 운영은 임시 공개형이며, 장기 안정 운영은 아니다.
- 장기 운영으로 넘어가려면 결국 외부 인프라가 필요하다.

즉, 이 프로젝트는 "기획 단계"가 아니라 "실사용 가능한 파일럿 단계"까지는 올라와 있다.
