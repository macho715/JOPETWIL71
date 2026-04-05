# JPT71 Voyage Command Center — AI 기능 업그레이드 아이디어 (문서 기준)

**기준 문서**: `myagent-copilot-kit/docs` (00-INDEX, 08-다른-프로젝트-적용-절차, 05-보안-운영-가이드, standalone-package/README)  
**대상**: `dashboard_final/JPT71_Voyage_Command_Center_Merged.html`  
**작성일**: 2026-03-10  
**스킬**: project-upgrade (Evidence + Best3 Deep)

---

## STANDALONE 조건 (전제)

본 업그레이드 아이디어는 **Standalone 우선**을 전제로 한다. OpenClaw 제품/게이트웨이 경유는 사용하지 않는다.

| 조건 | 내용 |
|------|------|
| **실행 기준** | `myagent-copilot-standalone` 패키지만 사용. OpenClaw CLI/앱/세션 미실행. |
| **공인 API** | `GET /api/ai/health`, `POST /api/ai/chat` 만 사용. |
| **엔드포인트** | 로컬: `http://127.0.0.1:3010`. 퍼블릭 시 HTTPS + `MYAGENT_PROXY_AUTH_TOKEN`, `MYAGENT_PROXY_CORS_ORIGINS`. |
| **인증** | 프록시 측: GitHub device login → `~/.myagent-copilot/auth-profiles.json`, runtime token cache. 대시보드는 프록시에 HTTP 요청만 보냄. |
| **payload** | 요약 JSON만 전송. 전체 raw dataset·heatmap 배열·개인정보 미전송. |
| **모델** | `github-copilot/gpt-5-mini` (문서 기준값 유지). |
| **호환 경로** | OpenClaw auth fallback은 **기준 아님**. 대시보드 연동은 Standalone proxy 단일 경로만 가정. |

*출처: standalone-package/README.md §1 패키지 개요, §9 환경변수, §12 API.*

---

## 1. Executive Summary

JPT71 Voyage Command Center 대시보드는 현재 **AI 연동이 없으며**, Heatmap/KPI/Fuel/RootCause 통합 뷰와 기간 필터·탭 구조만 제공한다. **STANDALONE 조건** 하에, **myagent-copilot-kit/docs** 및 **standalone-package/README** 기준으로 동일 키트의 Copilot 프록시(`GET /api/ai/health`, `POST /api/ai/chat`)만 사용해 **요약 JSON만 전송**하는 AI 패널을 추가하는 업그레이드가 적합하다. OpenClaw 경유는 호환 경로로 두지 않고 Standalone 단일 경로만 전제한다. 본 보고서는 문서 규약(요약 전송, 프리셋 3~4개, plain text 응답, 로컬/퍼블릭 분기)을 준수하는 **Top 10 아이디어**와 **Best 3 Deep Report**를 제안하며, 적용은 코드 변경 없이 **제안 + 로드맵**만 수행한다.

---

## 2. Current State Snapshot

| 항목 | 내용 |
|------|------|
| **대상 파일** | `dashboard_final/JPT71_Voyage_Command_Center_Merged.html` |
| **스택** | Vanilla JS, Chart.js (inline), 단일 HTML, 빌드 없음 |
| **데이터** | `window.JPT71VoyageCostHeatmapData` → `DATA` (cost, kpiLens, fuelSnapshot, rootSnapshot) |
| **상태** | `state.startMonth`, `state.endMonth`, `state.activeTab`, `state.theme` |
| **기존 함수** | `filteredRows()`, `filteredSummary()` — 기간 필터 기반 집계 이미 존재 |
| **탭** | Executive(0), Monthly Synthesis(1), Cost Structure(2), KPI Explorer(3), Heatmap(4), Fuel(5), RootCause(6), Action Ideas(7) |
| **AI** | 없음 |
| **문서 기준** | 08: 요약 JSON만 전송, 프리셋 3~4개, `POST /api/ai/chat`, plain text 응답; 05: DLP·민감도·토큰; README: 엔드포인트·헤더·응답 구조 |
| **전제** | **STANDALONE 조건**: OpenClaw 미사용, standalone proxy 단일 경로 (상단 표 참조). |

**evidence_paths**: `myagent-copilot-kit/docs/00-INDEX.md`, `08-다른-프로젝트-적용-절차.md`, `05-보안-운영-가이드.md`, `standalone-package/README.md` (Sections 12, 9 환경변수)

---

## 3. Upgrade Ideas Top 10

| # | 아이디어 | 버킷 | Impact | Effort | Risk | Confidence | PriorityScore | Evidence (최소 1) |
|---|----------|------|--------|--------|------|------------|---------------|-------------------|
| 1 | **요약 JSON 빌더 함수 도입** (filteredSummary 기반, raw 제외) | Architecture/Modularity | 5 | 2 | 1 | 5 | **12.5** | E1, E2 |
| 2 | **AI 전용 탭 또는 패널 추가** (프리셋 3~4 + 자유 질문 + plain text 응답) | DX/Tooling | 5 | 3 | 2 | 5 | **4.2** | E1, E2, E4 |
| 3 | **POST /api/ai/chat 연동** (엔드포인트·헤더·body 문서 준수) | Reliability | 5 | 2 | 1 | 5 | **12.5** | E1, E3 |
| 4 | **로컬/퍼블릭 엔드포인트·토큰 분기** (window.__JPT71_AI_* ) | Security | 4 | 2 | 1 | 5 | **10** | E1, E3 |
| 5 | **에러·로딩·DLP 거부 UX** (AI proxy unavailable, 4xx, guard.dlpStatus) | Reliability/Observability | 4 | 2 | 1 | 5 | **10** | E1, E5 |
| 6 | **프리셋 프롬프트 4종** (원인 요약, 실행 액션, 리스크 점검, KPI vs Heatmap) | Docs/Process | 4 | 1 | 1 | 5 | **20** | E1, E4 |
| 7 | **Action Ideas 탭 내 AI 블록** (기존 탭 흐름 유지) | DX/Tooling | 4 | 2 | 2 | 4 | **4** | E1, E2 |
| 8 | **Health 체크 선호출** (GET /api/ai/health로 사용 가능 여부 표시) | Reliability/Observability | 3 | 1 | 1 | 5 | **15** | E1, E3 |
| 9 | **요약 스키마 문서화** (보낼 필드·보내지 말 필드 팀 합의) | Docs/Process | 3 | 1 | 1 | 5 | **15** | E1, E2 |
| 10 | **x-request-id·x-ai-sensitivity 고정** (internal, requestId UUID) | Security | 3 | 1 | 1 | 5 | **15** | E1, E3 |

*PriorityScore = (Impact × Confidence) / (Effort × Risk)*

---

## 4. Best 3 Deep Report

Best 3 선정: **#1 요약 JSON 빌더**, **#3 POST /api/ai/chat 연동**, **#6 프리셋 프롬프트 4종** (문서 직접 요구사항 + Evidence E1·E2·E3 충족).

---

### Best 1: 요약 JSON 빌더 함수 도입

**Goal**  
현재 화면(기간 필터) 기준으로 AI에 보낼 **최소 요약 객체**를 반환하는 단일 함수를 도입한다. `DATA`·heatmap 원본은 전송하지 않는다.

**Non-goals**  
전체 `DATA` 또는 `HEATMAP_SOURCE.heatmap`을 그대로 노출하는 API 추가, 서버 측 저장.

**Proposed Design**
- **Component**: `getAiSummaryPayload()` (또는 `buildAiPayload()`).
- **Input**: 기존 `state` (startMonth, endMonth) + `filteredSummary()` 결과 + `DATA.kpiLens`, `DATA.fuelSnapshot`, `DATA.rootSnapshot`의 일부 필드만.
- **Output**: 단일 JSON 객체. 예: `{ period: { start, end }, cost: { totalAed, blendedAedPerTon, peakMonth, peakMonthAed, sourceMix, topVoyages: top5 }, kpiLens: { totalCost, outliers }, fuelSnapshot: { totalFuel, blendedFuelTon }, rootSnapshot: { dominantRoute, anchorShare } }`.
- **Data flow**: `state` 변경 → `filteredSummary()` 호출 → `getAiSummaryPayload()`가 이 결과와 DATA 일부를 조합 → 호출부에서 `JSON.stringify(payload)` 후 messages[].content에만 주입.

**PR Plan**
- PR1: `getAiSummaryPayload()` 함수 추가, 단위 테스트(목 데이터로 키 존재·타입 검증).
- PR2: 08 문서 “보내도 되는 것 / 보내지 말 것”을 주석 또는 상단 문서 블록으로 대시보드 내 명시.
- PR3: (선택) payload 크기 상한 체크 및 초과 시 경고 로그.

**Tests**
- Unit: payload 키 존재, `topVoyages.length <= 5`, 원본 `DATA.cost.monthly` 미포함.
- Integration: 실제 `state` 변경 후 payload에 해당 기간만 반영되는지.
- Security: payload에 이메일/토큰 패턴 없음 (정적 스캔 또는 DLP 연동 테스트).

**Rollout & Rollback**
- Feature flag 없이 함수만 추가; AI 탭이 없으면 호출되지 않음. 롤백 시 AI 패널 제거 시 해당 함수만 미사용으로 둠.

**Risks & Mitigations**
- 요약 필드 추가 시 실수로 raw 포함 → 08 체크리스트 + 코드 리뷰로 “보내지 말 것” 검증.

**KPIs**
- Payload 크기(토큰 또는 바이트) 상한 준수, DLP block 0건(내부 수치만 포함).

**Dependencies / Migration traps**
- `filteredSummary()` 시그니처 변경 시 `getAiSummaryPayload()` 동기 수정 필요.

**Evidence**
- E1 (docs/08): “요약 JSON 스키마를 정의”, “필터/집계 요약만”.
- E2 (Minimal Valuable Context): 최소 컨텍스트로 성능·비용·환각 완화.

---

### Best 2: POST /api/ai/chat 연동

**Goal**  
대시보드에서 **Standalone 조건** 하에 myagent-copilot-standalone 프록시(OpenClaw 비경유)의 `POST /api/ai/chat`만 호출하여, 문서 규약에 맞는 요청(body·header)을 보내고 응답의 `result.text`를 plain text로 표시한다.

**Non-goals**  
스트리밍, 다른 모델/엔드포인트 직접 호출, 토큰/비용 표시.

**Proposed Design**
- **Components**: (1) `askAi(summaryPayload, userMessage)` — fetch to `window.__JPT71_AI_ENDPOINT__`, (2) UI: 전송 버튼/프리셋 클릭 시 `askAi(getAiSummaryPayload(), presetOrUserText)` 호출.
- **Interfaces**: Request: `{ model: "github-copilot/gpt-5-mini", sensitivity: "internal", messages: [ { role: "system", content: "…" }, { role: "user", content: "질문: …\n요약 JSON:\n" + JSON.stringify(payload) } ] }`. Headers: `Content-Type: application/json`, `x-request-id: crypto.randomUUID()`, `x-ai-sensitivity: "internal"`, (퍼블릭 시) `x-ai-proxy-token`.
- **Response handling**: `response.result.text` → UI plain text; `response.guard.dlpStatus === "block"` 또는 4xx → 사용자에게 짧은 오류 메시지.

**PR Plan**
- PR1: `askAi()` 구현 + 엔드포인트 기본값 `http://127.0.0.1:3010/api/ai/chat`, 헤더 고정.
- PR2: UI에 “AI Insight” 블록(버튼 + 응답 영역 + 로딩/에러).
- PR3: 퍼블릭 분기(`__JPT71_AI_PROXY_TOKEN__` 존재 시 헤더 추가).

**Tests**
- Unit: mock fetch로 body/message 구조 검증.
- Integration: 로컬 프록시 대면 health → chat 200 → result.text 존재.
- Security: DLP block 시 사용자 노출 메시지에 민감 payload 미포함.

**Rollout & Rollback**
- 엔드포인트 미설정 시 AI 블록 비활성화 또는 “AI 사용 불가” 메시지. 롤백: AI 블록 제거.

**Risks & Mitigations**
- CORS: 프록시 CORS_ORIGINS에 대시보드 origin 포함(03/04 문서).

**KPIs**
- 200 응답 시 result.text 렌더링 성공, 4xx/DLP 시 사용자 친화 메시지 표시.

**Evidence**
- E1 (README §12.2, 08 §5.1): body·헤더·응답 구조.
- E3 (Backend Proxy Pattern): 프록시 경유 호출로 키 보호·제어.

---

### Best 3: 프리셋 프롬프트 4종

**Goal**  
문서 08 “프리셋 3~4개”에 맞춰, JPT71 맥락에 맞는 **고정 프롬프트 4종**을 정의하고 UI에 버튼으로 노출한다. 시스템 프롬프트는 “주어진 JSON 밖 사실은 단정하지 말고, 숫자와 단위를 유지하라” 수준으로 통일한다.

**Non-goals**  
사용자 편집 가능한 시스템 프롬프트, 다국어 전환.

**Proposed Design**
- **Components**: 상수 테이블 `AI_PRESETS = [ { id: "cause", label: "원인 요약", userPrompt: "선택 기간 비용·KPI·Fuel 요약을 보고 상위 원인 3가지를 한글로 짧게 요약해줘." }, { id: "action", label: "실행 액션", userPrompt: "이 요약 기준으로 비용 절감을 위한 실행 가능한 액션 3단계로 정리해줘." }, { id: "risk", label: "리스크 점검", userPrompt: "Fuel/RootCause 스냅샷을 보고 운영상 주의할 점을 3가지 이하로 짧게 적어줘." }, { id: "kpi-vs-heatmap", label: "KPI vs Heatmap", userPrompt: "KPI total cost와 Heatmap aggregate 차이가 나는 이유를 이 수치 기준으로 2~3문장으로 설명해줘." } ]`.
- **Data flow**: 버튼 클릭 → `askAi(getAiSummaryPayload(), preset.userPrompt)` → 응답 plain text 표시.

**PR Plan**
- PR1: `AI_PRESETS` 상수 + 시스템 프롬프트 1개(문서와 동일 문구) 정의.
- PR2: UI에 4개 버튼 + 자유 질문 입력(선택) + 응답 영역.
- PR3: 08/07 검증 체크리스트에 “프리셋 4종 동작” 항목 추가.

**Tests**
- Unit: 각 preset.userPrompt이 비어 있지 않음, 시스템 프롬프트에 “JSON” 포함.
- Manual: 각 버튼 클릭 시 동일 payload로 서로 다른 지시가 전달되는지.

**Rollout & Rollback**
- 기존 탭에 영향 없음. 롤백 시 버튼·핸들러 제거.

**Risks & Mitigations**
- 프롬프트 변경 시 운영 문서와 동기화(07 문서 정합성).

**KPIs**
- 4개 프리셋 모두 200 응답 시 유의미한 plain text 반환.

**Evidence**
- E1 (08 §4): “프리셋 버튼 3개 (원인 요약, 실행 액션, 리스크 점검)”.
- E4 (Preset patterns): 대시보드에서 프리셋으로 LLM 설정/용도 분리.

---

## 5. Options A/B/C

| 옵션 | 내용 | Risk | Time (추정) |
|------|------|------|-------------|
| **A (보수)** | Best 3만 적용: 요약 빌더 + chat 연동 + 프리셋 4종. AI는 단일 탭 또는 Action Ideas 내 1블록. | 낮음 | 2~3주 |
| **B (중간)** | A + Health 선호출(#8) + 에러/로딩/DLP UX(#5) + 로컬/퍼블릭 분기(#4). | 중간 | 3~4주 |
| **C (공격)** | B + 요약 스키마 문서화(#9) + request-id/sensitivity 고정(#10) + 07 검증 체크리스트 반영. | 낮음 | 4~5주 |

---

## 6. 30/60/90-day Roadmap (PR-sized)

- **30일**: PR1 요약 빌더, PR2 chat 연동 + AI 블록 UI, PR3 프리셋 4종 상수·버튼. 로컬 프록시로 스모크 테스트.
- **60일**: Health 선호출, 에러/로딩/DLP 메시지, `__JPT71_AI_ENDPOINT__`/`__JPT71_AI_PROXY_TOKEN__` 분기. 07 검증 체크리스트 1회 수행.
- **90일**: 요약 스키마 문서(대시보드 내 또는 docs), 08/07 정합성 검증, (선택) payload 상한·감사 로그.

---

## 7. Evidence Table

| ID | platform | title | url | published_date | updated_date | accessed_date | popularity_metric | why_relevant |
|----|----------|-------|-----|----------------|--------------|---------------|-------------------|--------------|
| E1 | official (project) | 다른 프로젝트 적용 절차 | myagent-copilot-kit/docs/08-다른-프로젝트-적용-절차.md | 2026-03-10 | — | 2026-03-10 | — | 요약만 전송, 프리셋 3~4, fetch 예시, JPT71 패턴 |
| E2 | official (project) | 문서 인덱스·기본값 | myagent-copilot-kit/docs/00-INDEX.md | 2026-03-10 | — | 2026-03-10 | — | 엔드포인트·모델·적용 순서 |
| E3 | official (project) | standalone-package README §12 | myagent-copilot-kit/standalone-package/README.md | 2026-03-10 | — | 2026-03-10 | — | POST /api/ai/chat 요청/응답 예시 |
| E4 | web | Preset Prompts UI / Presets in Dashboards | OpenRouter Presets, MLflow prompt UI (search snippet) | — | — | 2026-03-10 | — | 대시보드에서 프리셋으로 용도 분리 |
| E5 | web | Backend Proxy Pattern, LLM Integration | AIConexio / Frontend Digest (search snippet) | — | — | 2026-03-10 | — | 프록시 경유·로딩/에러 UX |
| E6 | web | Minimal Valuable Context (MVC) | adi.the-ihor.com (Minimal Valuable Context) | — | — | 2026-03-10 | — | 최소 컨텍스트로 비용·환각 감소 |

---

## 8. AMBER_BUCKET

- **E4, E5, E6**: 외부 검색 결과로 **published_date** 미확보. Top 10 점수·Best 3 선정에는 **E1~E3(문서)** 만으로도 충족하므로, E4~E6는 참고용으로만 사용하고 Best 3 Evidence는 E1·E2·E3 위주로 명시함.
- **GitHub Copilot API 공식 문서** (chat completions): URL 404로 확인 불가. 프로젝트 기준은 “standalone proxy의 POST /api/ai/chat”이므로 README·08이 SSOT.

---

## 9. Open Questions

1. **AI 패널 위치**: “AI Insight” 전용 탭 vs “Action Ideas” 탭 내 블록 — 팀 선호와 기존 탭 흐름 중 어느 쪽을 우선할지 결정 필요.
2. **퍼블릭 배포 시점**: 로컬 검증 후 퍼블릭(엔드포인트·토큰·CORS) 전환 일정이 정해지면 04·05 문서와 동기화할지 여부.
3. **요약 필드 확장**: 향후 Fuel/RootCause 상세를 더 넣을 경우, DLP(이메일/전화번호 등) 유입 가능성은 없으나 “보내지 말 것” 체크리스트를 언제 갱신할지.

---

*End of report. No code changes or commits were made; recommendations and roadmap only.*
