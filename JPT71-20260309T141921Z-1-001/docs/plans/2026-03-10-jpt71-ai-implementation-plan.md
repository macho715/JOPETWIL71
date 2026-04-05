# JPT71 AI 기능 — `dashboard_final` 구현 계획

**기준 대상**: `dashboard_final/JPT71_Voyage_Command_Center_Merged.html`  
**기준일**: 2026-03-10  
**상태**: `dashboard_final` 포팅 기준 구현 계획  
**레퍼런스**: `DASHBOARD/JPT71_Voyage_Command_Center_Merged.html`의 동작 패턴만 참조

---

## 1. 결정 사항 요약

이번 구현의 canonical 파일은 `dashboard_final/JPT71_Voyage_Command_Center_Merged.html`이다.

기존 초안의 아래 전제는 더 이상 사용하지 않는다.

- Executive 하단 접이식 AI 패널
- preset 4개만 제공
- 패널 첫 오픈 시 health gate
- 단일 HTML만 수정

이번 구현 기준은 아래로 고정한다.

- AI 위치: `Action Ideas` 탭 내부
- AI 구성: preset 10개 + 자유 질문 textarea + 전송 버튼 + 상태줄 + plain text 응답
- runtime/public 호환: `window.__JPT71_AI_ENDPOINT__`, `window.__JPT71_AI_PROXY_TOKEN__`
- companion 파일 허용: `dashboard_final/jpt71-runtime-config.js`
- health 선확인은 넣지 않고, 실제 요청 실패를 상태줄에 표시

---

## 2. 구현 범위

### 2.1 UI 배치

`Action Ideas` 패널 안에 AI 카드를 추가한다.

삽입 위치:

- `#actionCards` 바로 아래
- 읽는 순서 callout 바로 위

구성 요소:

- preset 버튼 10개
- `textarea` 1개, `maxlength=400`
- `질문 전송` 버튼
- 상태 텍스트 영역
- `<pre>` 기반 plain text 응답 영역

preset ID는 아래로 고정한다.

- `priority`
- `next-path`
- `brief`
- `confidence`
- `compare`
- `driver-shift`
- `cause`
- `actions`
- `risk`
- `gap`

### 2.2 상태 관리

`state.ai`를 추가한다.

```js
{
  loading: false,
  status: "idle",
  statusText: "현재 선택 기간 기준으로 AI 질문을 보낼 수 있습니다.",
  responseText: "",
  lastAskedPeriod: null
}
```

동작 규칙:

- 요청 중에는 preset 버튼과 전송 버튼을 비활성화한다.
- 성공 시 `lastAskedPeriod`를 현재 기간 키로 갱신한다.
- 필터 변경 후 기존 응답은 유지한다.
- 단, `lastAskedPeriod !== currentPeriodKey()`이면 상태줄에 “이전 기간 기준” 경고를 띄운다.

### 2.3 runtime/public 호환

HTML head에 `./jpt71-runtime-config.js`를 선로딩한다.

companion 파일:

- `dashboard_final/jpt71-runtime-config.js`

기본 내용:

- `window.__JPT71_AI_ENDPOINT__` 미설정 시 빈 문자열 유지
- `window.__JPT71_AI_PROXY_TOKEN__` 미설정 시 빈 문자열 유지

endpoint 해석 규칙:

```js
window.__JPT71_AI_ENDPOINT__ || "http://127.0.0.1:3010/api/ai/chat"
```

header 규칙:

- 항상 `Content-Type: application/json`
- 항상 `x-request-id`
- 항상 `x-ai-sensitivity: internal`
- token이 있으면 `x-ai-proxy-token`
- endpoint 호스트가 `ngrok.app` 또는 `ngrok-free.app`면 `ngrok-skip-browser-warning: true`

---

## 3. AI 요청 및 payload 설계

### 3.1 시스템 프롬프트

```js
"주어진 요약 JSON 밖 사실은 단정하지 말고, 숫자/단위/기간 표기를 유지하라. 한국어 plain text로 간결하게 답하라."
```

### 3.2 요청 형식

`askAi(question, presetId)`는 아래 형식으로만 `POST /api/ai/chat`을 호출한다.

```json
{
  "model": "github-copilot/gpt-5-mini",
  "sensitivity": "internal",
  "messages": [
    { "role": "system", "content": "..." },
    { "role": "user", "content": "질문: ...\n요약 JSON:\n..." }
  ]
}
```

응답 처리:

- 성공: `result.text`만 사용
- 실패: `detail -> error -> HTTP nnn`
- 네트워크 `TypeError`: `AI proxy unavailable`
- 빈 질문: `질문을 입력해 주세요.`

응답 렌더링:

- 반드시 `textContent`
- `innerHTML` 사용 금지

### 3.3 기본 payload

`getAiSummaryPayload(summary, presetId)`는 아래 필드만 반환한다.

```js
{
  context: { dashboard: "JPT71 Voyage Command Center", panel: "Action Ideas" },
  period: { startMonth, endMonth },
  executive: {
    filteredVoyages,
    filteredTon,
    filteredTotalAed,
    blendedAedPerTon,
    dominantSource,
    peakMonth,
    worstMonth,
    bestMonth
  },
  sourceMix: [{ name, totalAed, sharePct }],
  topVoyages: [{ voyage, month, totalAed, aedPerTon }],
  kpiLens: { totalCost, outliers, outlierFence },
  fuelSnapshot: { totalFuel, blendedFuelTon, avgDaily },
  rootSnapshot: { dominantRoute, dominantRouteShare, anchorShare, weightedFuelTrip }
}
```

제약:

- `topVoyages`는 최대 5개
- 아래 항목은 절대 미포함
  - `DATA.cost.monthly` 전체
  - raw heatmap 배열
  - 원본 iframe 문서 데이터
  - 개인정보, 토큰, 인증정보

### 3.4 선택적 확장 payload

`compare` preset일 때만 `comparison`을 추가한다.

```js
{
  baselinePeriod,
  currentTotalAed,
  baselineTotalAed,
  currentBlendedAedPerTon,
  baselineBlendedAedPerTon,
  deltaAed,
  deltaAedPerTon,
  dominantSourceCurrent,
  dominantSourceBaseline
}
```

baseline 규칙:

- 현재 선택 기간과 길이가 같은 직전 가용 기간
- 가용 월이 부족하면 `null`

`driver-shift` preset일 때만 `driverShift`를 추가한다.

```js
{
  focusMonth,
  priorComparableMonth,
  blendedDelta,
  topSourceChanges: [{ source, deltaAed, deltaSharePct }]
}
```

driver-shift 규칙:

- `focusMonth = worstMonth 우선, 없으면 peakMonth`
- `priorComparableMonth = focusMonth 직전의 가용 월`
- `topSourceChanges`는 상위 3개

중요:

- `DASHBOARD` 구현의 `reconciliation` payload는 `dashboard_final`에 그대로 옮기지 않는다.
- `dashboard_final`은 Heatmap aggregate + KPI Lens + Fuel/RootCause snapshot 구조를 유지한다.

---

## 4. 구현 단계

### Step 1

`dashboard_final/JPT71_Voyage_Command_Center_Merged.html` head에 runtime config script를 추가한다.

### Step 2

`dashboard_final/jpt71-runtime-config.js`를 추가한다.

### Step 3

`state.ai`, `AI_PRESET_PROMPTS`, `AI_SYSTEM_PROMPT`, `AI_DEFAULT_ENDPOINT`를 추가한다.

### Step 4

기간 요약 보조 함수와 AI payload 함수를 추가한다.

필수 함수:

- `rowsForPeriod(startMonth, endMonth)`
- `summarizePeriod(startMonth, endMonth)`
- `currentPeriodKey()`
- `getPeriodWindow()`
- `getBaselineWindow()`
- `getMonthSourceSnapshot()`
- `buildComparisonPayload()`
- `buildDriverShiftPayload()`
- `getAiSummaryPayload(summary, presetId)`

### Step 5

runtime/public request 보조 함수를 추가한다.

필수 함수:

- `resolveAiEndpoint()`
- `resolveAiProxyToken()`
- `shouldSendNgrokBypassHeader(endpoint)`
- `createRequestId()`
- `askAi(question, presetId)`

### Step 6

`Action Ideas` 탭에 AI 패널 HTML을 삽입한다.

### Step 7

`renderAiPanel()`을 추가하고 `renderAll()`에서 항상 호출한다.

### Step 8

`bindEvents()`에 아래 이벤트를 추가한다.

- preset 클릭
- 전송 버튼 클릭
- `Ctrl/Cmd+Enter` 전송

---

## 5. 검증 기준

### 5.1 수동 기능 검증

- `Action Ideas` 탭에 AI 카드가 보인다.
- 위치가 `actionCards` 아래, 읽는 순서 callout 위다.
- preset 10개가 모두 보인다.
- textarea는 400자 제한이다.
- `질문 전송`과 `Ctrl/Cmd+Enter`가 모두 동작한다.
- 응답은 HTML이 아니라 plain text만 표시된다.

### 5.2 payload 검증

- `getAiSummaryPayload()` 결과에 `monthly`, `heatmap`, raw dataset, iframe 문서 내용이 없다.
- `topVoyages.length <= 5`
- `compare` preset에서만 `comparison`이 생긴다.
- `driver-shift` preset에서만 `driverShift`가 생긴다.

### 5.3 네트워크 검증

- endpoint 미지정 시 `http://127.0.0.1:3010/api/ai/chat`
- `window.__JPT71_AI_PROXY_TOKEN__`이 있으면 `x-ai-proxy-token` 헤더가 붙는다.
- ngrok endpoint일 때만 `ngrok-skip-browser-warning`이 붙는다.
- 성공 시 `result.text`가 상태줄과 응답 영역에 반영된다.

### 5.4 오류/상태 검증

- 빈 질문은 `질문을 입력해 주세요.`
- 네트워크 실패는 `AI proxy unavailable`
- 비-200 응답은 `detail` 또는 `error`를 우선 노출
- 필터를 바꾸면 기존 응답은 남고 상태줄에 “이전 기간 기준” 안내가 뜬다.

---

## 6. 가정과 제외 범위

가정:

- `dashboard_final`이 이번 구현의 canonical 파일이다.
- `DASHBOARD` 파일은 reference implementation일 뿐 산출물 기준이 아니다.
- public deployment pack, Vercel pack, live status 문서는 이번 범위에 포함하지 않는다.

제외:

- health 선확인 게이트
- public share pack 재생성
- `dashboard_final/JPT71_AI_Upgrade_Report.md` 자동 동기화
- 별도 빌드 시스템, 프레임워크, 외부 의존성 추가

---

*이 문서는 현재 repo에서 실제 구현하려는 상태를 기준으로 재작성한 계획 문서다.*
