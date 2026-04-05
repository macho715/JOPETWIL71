> 표준 AGENTS.md 템플릿(복붙용, “명령 우선/경계 명확”)

# AGENTS.md

> Updated: 2026-03-01 (Asia/Dubai)
> Purpose: Give coding agents the minimum non-inferable context to work safely and fast.  

## 1) Setup / Commands (run these first)

- Install deps: `<CMD_INSTALL>`
- Dev server: `<CMD_DEV>`
- Build: `<CMD_BUILD>`
- Test: `<CMD_TEST>`
- Lint: `<CMD_LINT>`
- Format: `<CMD_FORMAT>`

## 2) Project structure (only what agents can’t infer quickly)

- Entry points:
  - `<path/to/main_entry>`
- Key modules:
  - `<path/to/core_module_1>` — <one-line purpose>
  - `<path/to/core_module_2>` — <one-line purpose>
- Config:
  - `<path/to/config>` — <what it controls>

## 3) Working agreements (minimal, enforceable)

- Always run: `<CMD_TEST>` after code changes.
- For PRs: run `<CMD_LINT>` and `<CMD_BUILD>` before opening.
- If a task needs new dependencies: **ask before adding**.

## 4) Boundaries (DO NOT TOUCH)

- Never modify:
  - `<path/to/secrets_or_prod_configs>`
  - `<path/to/vendor_or_generated>`
- Never commit secrets/keys/tokens. If found, stop and report.
- Do not change CI/workflows unless explicitly requested.

## 5) Code style (show examples, not essays)

- Language: `<LANG + VERSION>`
- Style:
  - `<rule_1>`
  - `<rule_2>`
- Example snippet:
  ```<lang>
  <paste 10~30 lines of “good style” code here>
  ```

## 6) Git / release workflow

- Branch: `<branch convention>`
- Commit message: `<convention>`
- PR checklist:
  - [ ] tests pass
  - [ ] lint pass
  - [ ] update docs if behavior changed

---

**작성 원칙(성공 패턴):**
- “명령을 앞에”, “역할/스택을 구체적으로”, “경계(하지 말 것)를 강하게”, “6개 코어 영역을 커버”가 성공률이 높다고 정리됩니다. :contentReference[oaicite:10]{index=10}  
- GeekNews 요약에서도 “자동 생성(/init)로 컨텍스트를 부풀리면 비용↑/성능↓, **비추론 정보만** 넣어라”가 반복됩니다. :contentReference[oaicite:11]{index=11}  

---

## 5) 적용 옵션 A/B/C (비용/리스크/시간)

| 옵션 | 산출물 | 장점 | 리스크 | 예상 소요 |
|---|---|---|---|---|
| **A. Minimal** | `AGENTS.md`만 | 가장 단순, 도구 호환 폭 넓음 | 도구별 세부 기능(Claude/Gemini 전용) 반영 부족 | 30~60분 |
| **B. Cross-tool** | `AGENTS.md` + `CLAUDE.md` + `GEMINI.md` | Claude는 CLAUDE.md, Gemini는 GEMINI.md 우선 규칙까지 정교화 가능 | 문서 간 규칙 충돌 가능 → QA 필요 | 60~120분 |
| **C. Enterprise** | B + 하위폴더 AGENTS 분리 + CI 점검 | 모노레포/멀티팀에서 유지보수 최적 | 운영 체계 없으면 “컨텍스트 부패” 발생 | 1~3일 |

- Claude는 **CLAUDE.md를 세션 시작에 읽음**. :contentReference[oaicite:12]{index=12}  
- Gemini(Android Studio)는 **AGENTS.md 스캔**, 그리고 같은 디렉터리의 **GEMINI.md가 우선**. :contentReference[oaicite:13]{index=13}  

---

## 6) QA 체크리스트(운영 Fail-safe)

**정확성**
- [ ] 모든 커맨드가 실제 존재하는가(package.json/Makefile/pyproject 등)
- [ ] 경로가 실제 존재하는가
- [ ] OS/버전/패키지매니저가 프로젝트 현실과 일치하는가

**안전/보안**
- [ ] secrets/infra/vendor/generated 등 **금지영역**이 명시돼 있는가
- [ ] “의존성 추가/CI 변경은 승인 필요”가 명시돼 있는가

**효율(토큰/성능)**
- [ ] 코드로 추론 가능한 설명(폴더 나열/장황한 아키텍처 설명)을 줄였는가
- [ ] 길면 하위 폴더로 분리했는가(Codex는 기본 32KiB 제한) :contentReference[oaicite:14]{index=14}  

---

## 7) 로드맵(Prepare→Pilot→Build→Operate→Scale)

1) **Prepare (D0)**  
- 템플릿/체크리스트를 “agents.md 프로젝트” 소스로 고정(Projects 기능) :contentReference[oaicite:15]{index=15}  

2) **Pilot (D1~D2)**  
- 최근 1개 레포로 AGENTS.md 작성 → 에이전트(Claude/Codex/Gemini) 3개 태스크로 A/B 비교

3) **Build (W1)**  
- 모노레포면 `apps/*`, `packages/*` 하위에 **부분 AGENTS.md** 배치

4) **Operate (상시)**  
- 커맨드/경로 변경 시 AGENTS.md 동시 업데이트(“컨텍스트 부패” 방지)

5) **Scale (월간)**  
- 팀 공통 규칙은 루트, 팀/모듈 규칙은 하위 디렉터리로 분리(충돌 최소화)

---

## Evidence Table (핵심 주장 근거)

| Claim | Source | Date | Evidence |
|---|---|---:|---|
| Projects는 프로젝트 단위로 파일/지침을 컨텍스트로 유지 | OpenAI Help: Projects in ChatGPT | (페이지 기준) | Project instructions/파일 추가/소스 저장 설명 :contentReference[oaicite:16]{index=16} |
| Codex는 AGENTS.md를 작업 전에 읽고, 체인/용량 제한이 있음 | OpenAI Dev: AGENTS.md guide | (페이지 기준) | 탐색/병합 순서 + 32KiB 기본 제한 :contentReference[oaicite:17]{index=17} |
| Claude Code는 루트 CLAUDE.md를 세션 시작에 읽음 | Anthropic: Claude Code overview | (페이지 기준) | “CLAUDE.md… reads at the start of every session” :contentReference[oaicite:18]{index=18} |
| Gemini(Android Studio)는 AGENTS.md를 상위 디렉터리까지 스캔, GEMINI.md 우선 규칙 존재 | Android Developers: agent files | 2025-09-04 | 스캔 방식 + GEMINI.md precedence 명시 :contentReference[oaicite:19]{index=19} |
| 잘 되는 agents.md는 “명령 우선/경계 명확/6개 코어 영역”이 공통 | GitHub Blog 분석 | 2025-11-19 | 2,500+ 레포 분석 기반 베스트 프랙티스 :contentReference[oaicite:20]{index=20} |
| 자동 생성으로 컨텍스트를 부풀리면 비용↑/성능↓ → 비추론 정보만 넣어라 | GeekNews 요약 | 2026-02-?? | /init 자동 생성 경고 요지 :contentReference[oaicite:21]{index=21} |

---

