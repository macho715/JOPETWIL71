# JPT71 Voyage Command Center — AI 기능 구현 플랜 (Plan Doc)

**문서 유형**: Plan Doc (project-plan 스킬 산출물)  
**입력 출처**: `dashboard_final/JPT71_AI_Upgrade_Report.md`  
**작성일**: 2026-03-10  
**전제**: STANDALONE 조건, OpenClaw 미사용

---

## Input Gate (필수 입력 요약)

| 항목 | 출처 |
|------|------|
| Current State Snapshot | Report §2 |
| Selected Ideas | Best 3 (#1 요약 빌더, #3 chat 연동, #6 프리셋 4종) + Top 10 표 |
| Evidence Table | Report §7 (E1~E6, E4~E6 AMBER) |

**브레인스토밍 합의(반영)**  
- AI 패널 위치: **Executive 탭 하단 접이식 패널** (기본 접힘).  
- 입력: **프리셋 4개 버튼 + 자유 질문 1줄**.  
- 프록시 불가 시: 패널 열었을 때만 "AI 사용 불가" 표시, **Health 체크는 패널 첫 오픈 시 1회**.

---

## A. UI/UX

### A.1 정보 구조(IA) · 사용자 플로우
- Executive 탭 진입 → 기존 카드/차트 확인 → **하단 접이식 “AI Insight” 블록** 헤더 클릭 시 패널 열림.
- 패널 열림 시: (1) **최초 1회** `GET /api/ai/health` 호출 → 성공 시 버튼/입력 활성화, 실패 시 “AI 사용 불가” 문구 + 버튼/입력 비활성화. (2) 프리셋 4개 버튼 또는 자유 질문 입력 후 전송 → 응답 plain text 표시.
- 사용자 플로우: [Executive 탭] → [AI 패널 열기] → [Health 확인] → [프리셋 클릭 또는 자유 질문 입력 후 전송] → [응답 읽기].

### A.2 화면/컴포넌트
- **접이식 패널**: 헤더(예: “AI Insight (선택 기간 요약 기준)”), 클릭 시 본문 토글. 기본 상태 **접힘**.
- **본문 구성**: (1) 프리셋 버튼 4개(원인 요약, 실행 액션, 리스크 점검, KPI vs Heatmap). (2) 자유 질문 1줄 입력 + 전송 버튼. (3) 응답 영역(plain text, 스크롤 가능). (4) 로딩 중 표시. (5) 오류 시 짧은 메시지(연결 실패 / 4xx / DLP 등).
- **비활성 상태**: Health 실패 시 버튼·입력 비활성화, “AI 프록시에 연결할 수 없습니다. 로컬에서 프록시를 실행한 뒤 새로고침하세요.” 문구 표시.

### A.3 접근성
- 버튼·입력에 적절한 label/aria. 접이식 헤더에 aria-expanded. 포커스 순서: 프리셋 → 자유 질문 입력 → 전송.

---

## B. 아키텍처

### B.1 컴포넌트
- **단일 파일**: `dashboard_final/JPT71_Voyage_Command_Center_Merged.html` 내에만 추가. 별도 JS/CSS 파일 없음.
- **데이터**: 기존 `state`, `DATA`, `filteredSummary()` 재사용. 신규: `getAiSummaryPayload()`(요약 객체 반환), `askAi(payload, userMessage)`(fetch + 응답 처리).
- **상수**: `AI_PRESETS`(4종), 시스템 프롬프트 1개, `AI_SYSTEM_PROMPT`.

### B.2 데이터 흐름
- `state.startMonth/endMonth` 변경 → `filteredSummary()` → `getAiSummaryPayload()` → `askAi(payload, presetOrUserText)` → `POST /api/ai/chat` → `response.result.text` → UI plain text.
- 요약 payload에 **포함**: period, cost(집계·topVoyages 최대 5), kpiLens 일부, fuelSnapshot·rootSnapshot 일부. **미포함**: `DATA.cost.monthly` 전체, `HEATMAP_SOURCE.heatmap`, 개인정보.

### B.3 인터페이스
- **엔드포인트**: `window.__JPT71_AI_ENDPOINT__` 미설정 시 기본값 `http://127.0.0.1:3010/api/ai/chat`.
- **요청**: `{ model: "github-copilot/gpt-5-mini", sensitivity: "internal", messages: [ { role: "system", content: AI_SYSTEM_PROMPT }, { role: "user", content: "질문: ...\n요약 JSON:\n" + JSON.stringify(payload) } ] }`.
- **헤더**: `Content-Type: application/json`, `x-request-id: crypto.randomUUID()`, `x-ai-sensitivity: "internal"`. (퍼블릭 시 `x-ai-proxy-token` 추가.)
- **응답**: `result.text` 사용. `guard.dlpStatus === "block"` 또는 4xx 시 사용자에게 짧은 오류 메시지.

---

## C. 코드 구현 (모듈/파일/PR)

### C.1 모듈 경계
- 모든 로직은 동일 HTML 내 `<script>` 블록. 네임스페이스 분리 없음(기존 스타일 유지).

### C.2 파일/폴더 단위 PR 계획
- **PR1**: `getAiSummaryPayload()` 함수 추가. `filteredSummary()` 및 `DATA` 기반, topVoyages 최대 5, raw 미포함. (선택) 주석으로 “보내도 되는 것 / 보내지 말 것” 08 요약.
- **PR2**: `askAi(payload, userMessage)` 구현. fetch, 기본 엔드포인트, 헤더, body, 응답 파싱(`result.text`), 예외 시 사용자 메시지.
- **PR3**: Executive 탭 하단에 접이식 AI 패널 HTML + 이벤트(패널 열기 시 health 1회, 프리셋 클릭, 자유 질문 전송, 응답/로딩/에러 표시). `AI_PRESETS`, `AI_SYSTEM_PROMPT` 상수.
- **PR4**(선택): `__JPT71_AI_PROXY_TOKEN__` 존재 시 `x-ai-proxy-token` 헤더 추가. 엔드포인트/토큰 분기 정리.

---

## D. 테스트 / CI·CD / 관측

### D.1 테스트
- **Unit(수동/콘솔)**: `getAiSummaryPayload()` 반환 객체에 기대 키 존재, `topVoyages.length <= 5`, `DATA.cost.monthly` 미포함. `askAi` mock fetch 시 body/headers 구조 검증.
- **Integration**: 로컬에서 standalone 프록시 기동 후 Health → Chat 200 → `result.text` 표시 확인. 프리셋 4종 각 1회 호출.
- **보안**: payload에 이메일/토큰 패턴 없음(수동 또는 정적 검토).

### D.2 CI/CD
- 현재 대시보드는 빌드 없음. 변경 시 기존 HTML/JS 구문 오류 없음 확인(로컬 브라우저 또는 간단 스크립트).

### D.3 관측(Logs/Metrics/Tracing)
- 프록시 측: `openclaw.copilot.proxy.log.v1`(requestId, route, dlpStatus, latency). 대시보드 측: 별도 로깅 없음. (선택) 요청 실패 시 콘솔에 비민감 메시지.

---

## E. 에러 대응

### E.1 재시도 / 타임아웃
- fetch 실패 또는 타임아웃 시 1회 사용자 메시지 표시. 자동 재시도 없음(문서 권장 준수).

### E.2 사용자 메시지
- Health 실패: “AI 프록시에 연결할 수 없습니다. 로컬에서 프록시를 실행한 뒤 새로고침하세요.”
- 4xx: “요청이 거부되었습니다. 상태 코드: …”
- DLP block: “요청 내용이 정책에 의해 차단되었습니다.”
- 네트워크 오류: “네트워크 오류가 발생했습니다. 연결을 확인하세요.”

### E.3 Idempotency / Circuit breaker
- 미적용. 단일 사용자 대시보드, 요청당 1회 전송.

---

## F. 의존성 / 라이선스 / 마이그레이션

### F.1 의존성
- 기존: Chart.js(inline), Vanilla JS. **신규 런타임 의존성 없음.** 외부 서비스: myagent-copilot-standalone 프록시(로컬 3010 또는 퍼블릭 HTTPS).

### F.2 라이선스
- 기존 대시보드 라이선스 유지. 추가 라이브러리 없음.

### F.3 마이그레이션
- `filteredSummary()` 시그니처 변경 시 `getAiSummaryPayload()` 동기 수정 필요. 기존 탭/state 구조 변경 없음.

---

## G. 운영(Runbook) / Incident / 롤백

### G.1 Runbook
- 프록시 미동작 시: standalone-package `OPERATIONS.md` 및 `README` 참고. `pnpm serve:local` 또는 `node dist/cli.js serve`.
- 대시보드: 정적 HTML이므로 배포 경로만 확인. 엔드포인트/토큰은 `window.__JPT71_AI_*` 또는 인라인 기본값.

### G.2 Incident
- AI 패널만 오동작 시: 해당 블록 숨기거나 스크립트 분기로 비활성화. 프록시 장애는 06-장애대응-런북 참고.

### G.3 롤백 트리거
- AI 관련 코드 제거 시: 접이식 패널 HTML + `getAiSummaryPayload`, `askAi`, `AI_PRESETS`, health/이벤트 핸들러 제거. 기존 Executive 카드/차트는 변경 없음.

---

## H. 설계 결정(Decision) × 벤치마크

| Decision | 적용 범위 | 구현 접근 | Evidence |
|----------|-----------|-----------|----------|
| 요약만 전송 | getAiSummaryPayload | filteredSummary + DATA 일부, raw 미포함 | E1, E2 |
| POST /api/ai/chat 단일 호출 | askAi | fetch, 문서 body/header 준수 | E1, E3 |
| 프리셋 4 + 자유 질문 | UI | AI_PRESETS + 1줄 input | E1, E4 |
| Executive 하단 접이식 | UI | 패널 기본 접힘, 첫 오픈 시 health 1회 | (브레인스토밍 합의) |
| Health 실패 시 비활성화 | UX | 패널 열었을 때만 메시지, 버튼/입력 비활성 | E3, 08 |

*벤치마크: plan-benchmark-scout 백그라운드 실행. 결과 미도달 시 AMBER_BUCKET으로 격리.*

---

## I. Evidence Table (Ideas)

| ID | platform | title | url | published_date | accessed_date | why_relevant |
|----|----------|-------|-----|----------------|---------------|--------------|
| E1 | official (project) | 다른 프로젝트 적용 절차 | myagent-copilot-kit/docs/08-다른-프로젝트-적용-절차.md | 2026-03-10 | 2026-03-10 | 요약만 전송, 프리셋 3~4, fetch 예시 |
| E2 | official (project) | 문서 인덱스·기본값 | myagent-copilot-kit/docs/00-INDEX.md | 2026-03-10 | 2026-03-10 | 엔드포인트·모델 |
| E3 | official (project) | standalone-package README §12 | myagent-copilot-kit/standalone-package/README.md | 2026-03-10 | 2026-03-10 | POST /api/ai/chat 요청/응답 |
| E4 | web | Preset UI (참고) | — | — | 2026-03-10 | AMBER: 날짜 미확보. 프리셋 용도 분리 참고 |
| E5 | web | Proxy/LLM UX (참고) | — | — | 2026-03-10 | AMBER: 로딩/에러 UX 참고 |
| E6 | web | Minimal Context (참고) | — | — | 2026-03-10 | AMBER: 요약 최소화 참고 |

---

## J. Risk Register

| Risk | 영향 | 완화 |
|------|------|------|
| CORS 차단 | 퍼블릭 배포 시 chat 실패 | 프록시 `MYAGENT_PROXY_CORS_ORIGINS`에 대시보드 origin 포함(04 문서) |
| payload에 raw 유입 | DLP block 또는 과다 토큰 | getAiSummaryPayload에 monthly/heatmap 미포함, 코드 리뷰 |
| filteredSummary 시그니처 변경 | getAiSummaryPayload 오동작 | 변경 시 동기 수정, 의존성 명시 |
| 프록시 미기동 | 사용자 “사용 불가” 경험 | 첫 오픈 시 health 1회, 명확한 문구 |

---

## K. Delivery Plan (30/60/90 + PR-sized)

| 기간 | 내용 |
|------|------|
| **30일** | PR1 getAiSummaryPayload. PR2 askAi + 기본 엔드포인트/헤더. PR3 Executive 하단 접이식 패널 + 프리셋 4 + 자유 질문 + health 첫 오픈 1회 + 로딩/에러. 로컬 프록시 스모크 테스트. |
| **60일** | PR4(선택) 퍼블릭 분기(__JPT71_AI_PROXY_TOKEN__, 엔드포인트). 에러 메시지 세분화(4xx, DLP). 07 검증 체크리스트 1회. |
| **90일** | 요약 스키마 문서(보낼/보내지 말 필드) 대시보드 주석 또는 docs. 08/07 정합성 검증. (선택) payload 상한·감사 로그. |

---

## 파괴적 작업 게이트

- **파괴적 작업 없음.** 기존 탭/차트/state 제거 또는 대체 없음. 추가만 수행.
- 변경 범위: 단일 파일 `JPT71_Voyage_Command_Center_Merged.html` 내 추가. dry-run: 해당 파일에만 diff 발생하는지 확인. 적용 전 change list 검토 권장.

---

## AMBER_BUCKET

- E4, E5, E6: published_date 미확보. 핵심 설계 근거는 E1~E3.
- 벤치마크(plan-benchmark-scout) 결과: 별도 수신 시 본 문서 Evidence Table에 병합. 미수신 시 본 플랜은 Report + 브레인스토밍 합의만으로 유효.

---

*End of Plan Doc. No code changes or commits by this skill.*
