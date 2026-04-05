
아래는 **project-upgrade** 스킬에 따른 **JPT71/invoice_decklog** 스코프의 **UPGRADE_REPORT** 요약본입니다. (Ask 모드: 문서만 제안, 코드/설정 변경 없음.)

---

# UPGRADE_REPORT — JPT71/invoice_decklog

## 1. Executive Summary

- **범위**: `JPT71/invoice_decklog` — OFCO·decklog·jpt71 엑셀 기반 운영 보고서 + Data Spine(Scorecard, Leakage, Exception, Manifest).
- **현재 상태**: Python 3.11+, pandas + openpyxl, YAML 설정, 타입 힌트 일부 사용, **테스트/CI 없음**, **구조화 로깅 없음**.
- **제안**: 신뢰성(테스트·검증)·관찰성(로깅)·설정·DX(타입·스키마)·문서화 5개 버킷에서 Top10 아이디어 도출, Best3 Deep(테스트·로깅·Excel 계약 강화) 제안. Evidence는 가능한 경우 2025-06+ EN 자료로 연결했으며, 날짜 불명확 자료는 AMBER_BUCKET에 구분 기재.

---

## 2. Current State Snapshot (Doc-first)

| 항목 | 내용 |
|------|------|
| **진입점** | `jpt71_ops_report.py` (argparse, `main()` → MD/Excel), `jpt71_spine.py` (run_spine) |
| **입력** | `ofco detail.xlsx` (OFCO INVOICE ALL), `decklog.xlsx` (첫 시트), `jpt71.xlsx` (Sheet2), `INVOICE.xlsx` (선택), `TagMap_v1.1.csv`, `config_jpt71_report.yml` |
| **출력** | `out/JPT71_ops_report.md`, `out/JPT71_ops_summary.xlsx` (다수 시트), `out/run_manifest.json` |
| **의존성** | pandas, openpyxl, PyYAML (spine에서 optional); requirements.txt 미확인 |
| **테스트** | 없음 (pytest/test_* 미사용) |
| **CI** | 없음 (.github/workflows 등 미확인) |
| **로깅** | `print()` 위주, 구조화 로깅/JSON 로그 없음 |
| **설정** | `config_jpt71_report.yml` (config_version 1.0), dict 기반, Pydantic 미사용 |
| **타입** | 함수 시그니처에 타입 힌트 일부 있음, mypy/strict 미적용 |
| **문서** | README_report.md, DATA_CONTRACT.md, 보고서 작성 plan.md, JPT71 종합 리포트.md |

**evidence_paths**:  
`JPT71/invoice_decklog/jpt71_ops_report.py`, `jpt71_spine.py`, `config_jpt71_report.yml`, `README_report.md`, `DATA_CONTRACT.md`, `TagMap_v1.1.csv`, `보고서 작성 plan.md`, `JPT71 종합 리포트.md`

---

## 3. Stack / Constraints

| 구분 | 내용 |
|------|------|
| 언어/런타임 | Python 3.11+ (docstring 명시) |
| 데이터 | pandas, openpyxl (.xlsx), CSV (TagMap) |
| 설정 | YAML (PyYAML), config_version 1.0 |
| 배포/실행 | CLI 로컬 실행, 스케줄러/배포 미언급 |
| 제약 | 엑셀 시트/컬럼 계약(DATA_CONTRACT), OFCO/jpt71/decklog 파일명·시트명 고정 가정 |

---

## 4. External Research & Evidence

- **E1** TheLinuxCode, “Loading Excel Spreadsheets into pandas DataFrames: Practical Production Guide (2026)” — pandas 2.2+, openpyxl, Python 3.11+/3.12, read_excel 계약화·스키마 검증·fixture 테스트·로깅 권고. *(published_date 미명시 → AMBER_BUCKET)*  
- **E2** Data Pipeline Testing (e.g. dataengineeringcompanies.com “10 Actionable Data Pipeline Testing Best Practices for 2026”) — E2E/품질/단위·통합 테스트 계층, pytest, fixture·mock. *(날짜 2025-06+ 미확인 → AMBER_BUCKET)*  
- **E3** Pydantic V2 — ConfigDict, BaseModel, pydantic-settings; 2025년 기준 프로덕션 권장. *(공식 문서, 버전 기준으로 채택)*  
- **E4** structlog — JSON 렌더러, 25.x (2025), 프로덕션 로깅 권장. *(버전만 명시, published_date 없음 → AMBER_BUCKET)*  
- **E5** MyPy strict — strict=true, disallow_untyped_defs 등; Shiriev 2025-02-07 게시. *(2025-02 < 2025-06 → AMBER_BUCKET)*  

→ **날짜 충족 Evidence**: E3 (Pydantic).  
→ **AMBER_BUCKET**: E1, E2, E4, E5 (원본 published/updated_date 부재 또는 2025-06 미만).

---

## 5. Upgrade Ideas Top 10 (6 buckets)

| # | Bucket | Idea | PriorityScore (Impact×Confidence)/(Effort×Risk) | Evidence |
|---|--------|------|--------------------------------------------------|----------|
| 1 | Reliability | Excel 로더에 fixture 기반 pytest 추가 (필수 컬럼·dtype·샘플 시트) | 높음 | E1, E2 |
| 2 | Reliability | read_excel 호출에 sheet_name/header/usecols/dtype 명시 및 DATA_CONTRACT와 정렬 | 높음 | E1, DATA_CONTRACT.md |
| 3 | Security | 설정/비밀: .env + pydantic-settings, 비밀 로그 금지 | 중간 | E3, 보안 관행 |
| 4 | Performance | 대용량 decklog/OFCO 시 `nrows`/usecols 또는 1회 Parquet 스테이징 검토 | 중간 | E1 |
| 5 | DX | mypy --strict 단계 도입 (신규/수정 모듈부터), 타입 스텁 보강 | 중간 | E5 |
| 6 | DX | Pydantic 모델로 config_jpt71_report.yml 로드 (config_version, tagmap, mismatch, charter 등) | 높음 | E3 |
| 7 | Architecture | 로더/집계/쓰기 책임 분리 (read/validate → business logic → write) | 중간 | E1 |
| 8 | Docs | DATA_CONTRACT.md에 “필수 컬럼 집합” 및 실패 시 동작 명시, run_manifest 필드 설명 보강 | 낮음 | 현행 문서 |
| 9 | Reliability | run 시 품질 지표 로깅 (rows_read, unknown_rate, unmatched_count, null 핵심 컬럼 수) | 높음 | E1, E4 |
| 10 | DX | structlog 도입(JSON + console), 실행 요약·실패 시 traceback 구조화 로깅 | 높음 | E1, E4 |

- Evidence 부족/날짜 AMBER 항목은 Top10 채택 시 “권장 Evidence 추가”로 표시함.

---

## 6. Best 3 Deep Report (Evidence ≥2 또는 강한 1개 + AMBER 명시)

### Best #1: Fixture 기반 pytest로 Excel/Spine 계약 검증

- **Goal**: 엑셀 입력·스파인 출력에 대한 회귀 방지 및 계약 안정화.
- **Design**: `tests/` 하위에 `test_load_ofco.py`, `test_spine_integration.py` 등; 소형 fixture 엑셀(필수 컬럼만)·기대 시트/행 수/키 유니크; DATA_CONTRACT 필수 컬럼 assert.
- **PR Plan**: (1) tests/ + conftest.py 및 fixture 엑셀 추가, (2) load_ofco_detail / load_decklog 필수 컬럼 검증 테스트, (3) run_spine 스모크(고정 fixture → Scorecard/Leakage 행 수·컬럼 존재).
- **Tests**: 필수 컬럼 누락 시 ValueError, 동일 fixture에서 Scorecard 합계 불변.
- **Rollout/Rollback**: 기본은 로컬만; CI 연동 시 파이프라인 추가 후 롤백은 해당 job 비활성화.
- **Risks**: fixture가 실제 파일과 어긋나면 false positive 가능 → DATA_CONTRACT와 동기화 의무.
- **KPIs**: 커밋 전 pytest 통과, spine 변경 시 관련 테스트 1개 이상.
- **Evidence**: E1, E2 (E2 AMBER).

---

### Best #2: structlog + 실행 요약/품질 지표 로깅

- **Goal**: 배치 실패·품질 저하를 3AM에도 추적 가능하게.
- **Design**: structlog 설정(JSON 파일/콘솔), `jpt71_ops_report.py`/`jpt71_spine.py`에서 print 대신 logger; run 종료 시 rows_read, unknown_rate, unmatched_count, collision_count, outputs, run_id 등 구조화 로그 1건.
- **PR Plan**: (1) structlog 의존성 및 logger 설정 모듈, (2) main/run_spine에 로그 호출 추가, (3) run_manifest와 동일한 메타를 로그에 출력.
- **Tests**: 로그 출력을 캡처해 “run_id” 또는 “unknown_rate” 키 존재 assert.
- **Rollout/Rollback**: 로그 레벨/타겟만 변경하면 되므로 롤백 용이.
- **Risks**: 로그에 민감 필드 포함 금지(이미 run_manifest는 비밀 없음).
- **KPIs**: 매 run 구조화 로그 1건, 실패 시 traceback 로그.
- **Evidence**: E1, E4 (E4 AMBER).

---

### Best #3: Excel read 계약 명시 + DATA_CONTRACT 정렬

- **Goal**: read_excel을 “계약 경계”로 두고, 시트/헤더/컬럼/타입을 문서와 코드에서 일치.
- **Design**: 모든 read_excel에 sheet_name, header(또는 skiprows), usecols 또는 EXPECTED_COLUMNS 기반 검증; DATA_CONTRACT.md에 “Input sheets” 테이블 추가(시트명·필수 컬럼·타입).
- **PR Plan**: (1) DATA_CONTRACT에 입력 시트·필수 컬럼 명시, (2) load_ofco_detail/load_decklog/load_jpt71_sheet2_with_keys에 필수 컬럼 검증 및 명시적 read_excel 인자, (3) 누락 시 ValueError 메시지에 누락 컬럼명 포함.
- **Tests**: 필수 컬럼 누락 fixture로 ValueError 발생 테스트.
- **Rollout/Rollback**: 기존 파일이 계약을 만족하면 동작 동일; 불만족 시 의도적 실패.
- **Risks**: 기존 엑셀에 선택 컬럼이 없으면 즉시 실패 → 운영팀에 계약 공유 필요.
- **KPIs**: 계약 위반 시 1회 run 내 실패, 문서와 코드 일치.
- **Evidence**: E1, DATA_CONTRACT.md.

---

## 7. Options & Roadmap

- **Option A (최소)**: Best #3만 적용 — 계약 명시 + read_excel 정리.  
- **Option B (권장)**: Best #1 + #3 → 테스트 + 계약.  
- **Option C (전체)**: Best #1 + #2 + #3 → 테스트 + 로깅 + 계약.

**30/60/90-day Roadmap (예시)**  
- 30일: DATA_CONTRACT 입력 명세, read_excel 명시화, Best #3 적용.  
- 60일: tests/ 추가, fixture 및 Best #1 적용.  
- 90일: structlog 도입 및 실행 요약 로깅(Best #2), (선택) CI에서 pytest 실행.

---

## 8. Evidence Table (요약)

| ID | URL/소스 | published/updated | accessed | 비고 |
|----|----------|--------------------|----------|------|
| E1 | thelinuxcode.com (Excel production guide 2026) | 미명시 | 2026-03 | AMBER |
| E2 | data pipeline testing 2026 등 | 미명시 | 2026-03 | AMBER |
| E3 | pydantic.com (V2 config) | 2025+ | 2026-03 | OK |
| E4 | structlog 25.x | 2025 (월 미명시) | 2026-03 | AMBER |
| E5 | Strict Mypy (Shiriev) | 2025-02-07 | 2026-03 | AMBER (before 2025-06) |

---

## 9. AMBER_BUCKET

- **E1, E2, E4**: 원문에 published_date 또는 updated_date 없음 → Top10/Best3에서 “권장 Evidence”로 사용했으나, 공식 채택 시 출처에 날짜 확인 후 교체 권장.  
- **E5**: 2025-02 게시로 2025-06+ 미충족 → AMBER.  
- **BEST3_INCOMPLETE 아님**: Best3 3개 모두 제안됨. 단, Evidence가 2개인 경우 일부 AMBER 포함.

---

## 10. Open Questions (≤3)

1. **CI**: pytest를 GitHub Actions 등에서 실행할지, 및 fixture 엑셀을 레포에 포함할지 여부.  
2. **의존성 고정**: requirements.txt 또는 pyproject.toml에 pandas/openpyxl 버전 고정 및 “ingestion smoke test in CI” 도입 여부.  
3. **PDF 인보이스**: `첨부 1. Invoice_(*).pdf`는 현재 파이프라인 미연동; 추후 OCR/추출 연동 시 보안·감사 로깅 요구사항 정리 필요.

---

## 11. Web Scout Results (2025-06+ Evidence)

Evidence below was gathered to replace or supplement E1, E2, E4, E5 with sources that have **published_date or updated_date ≥ 2025-06-01**. Only items with a confirmed date in that range are listed as TOP_HIT; items without a date or with date before 2025-06-01 are listed under AMBER with reason.

### Evidence Table

| Evidence ID | URL | Title | published_date or updated_date | relevance | TOP_HIT / AMBER |
|-------------|-----|-------|-------------------------------|-----------|------------------|
| E6 | https://pandas.pydata.org/docs/whatsnew/v2.3.1.html | What's new in 2.3.1 (July 7, 2025) — pandas documentation | 2025-07-07 | Official pandas release notes; IO/dtype/Excel ecosystem and production behavior; supports read_excel contract and schema/dtype practices. | TOP_HIT |
| E6b | https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html | pandas.read_excel — pandas 3.0.1 documentation | 2026-02-17 (doc set) | Canonical API for read_excel (sheet_name, header, usecols, dtype, engine); aligns with Best3 Excel read contract and E1 topic. | TOP_HIT |
| E7 | https://pypi.org/project/pytest-regressions/ | pytest-regressions (PyPI; 2.8.1 release) | 2025-07-04 | Golden-file / regression fixtures (data_regression, dataframe_regression, file_regression) for data pipeline testing; supports Best1 fixture-based pytest. | TOP_HIT |
| E8 | https://github.com/hynek/structlog/releases/tag/25.4.0 | structlog 25.4.0 Release | 2025-06-02 | Production structlog release; JSON/structured logging, console vs production output; supports Best2 structlog adoption. | TOP_HIT |
| E9 | https://www.structlog.org/en/25.3.0/logging-best-practices.html | Logging Best Practices — structlog 25.3.0 documentation | 2025-04-25 (25.3.0 release) | JSON in production, stdout, canonical log lines; 25.3.0 < 2025-06-01 → use E8 for TOP_HIT; this doc supports E4 topic. | AMBER (doc version 25.3.0 released 2025-04-25, before 2025-06-01) |
| E10 | https://mypy-lang.blogspot.com/2025/07/mypy-117-released.html | Mypy 1.17 Released | 2025-07-14 | Official mypy release; type checking, strict mode context, Python 3.9+ requirement; supports Best3/DX mypy strict (E5 replacement). | TOP_HIT |

### AMBER_BUCKET (no date or date &lt; 2025-06-01)

| Evidence ID | URL | Title | reason |
|-------------|-----|-------|--------|
| — | https://johal.in/pytest-regressions-data-golden-file-updates-2025/ | Pytest Regressions Data: Golden File Updates 2025 | No explicit published_date (YYYY-MM-DD) on page. |
| — | https://johal.in/mypy-strict-mode-configuration-enforcing-type-safety-in-large-python-codebases/ | Mypy Strict Mode Configuration: Enforcing Type Safety in Large Python Codebases | No explicit published_date (YYYY-MM-DD) on page. |
| E9 | (see table above) | structlog 25.3.0 Logging Best Practices | Doc tied to 25.3.0 release 2025-04-25; before 2025-06-01. |

### Summary

- **E1 (Excel/pandas/openpyxl, read_excel contract, schema validation, fixture testing):** **2 TOP_HITs** — E6 (pandas 2.3.1 whatsnew 2025-07-07), E6b (pandas read_excel API 3.0.1 docs 2026-02-17). Each has explicit date ≥ 2025-06-01.
- **E2 (Data pipeline testing, pytest, fixtures, golden files):** **1 TOP_HIT** — E7 (pytest-regressions 2.8.1, 2025-07-04). AMBER: johal.in golden-file article (no date).
- **E4 (structlog JSON logging for Python production):** **1 TOP_HIT** — E8 (structlog 25.4.0 release 2025-06-02). AMBER: structlog 25.3.0 Logging Best Practices (release 2025-04-25).
- **E5 (mypy strict mode / type checking):** **1 TOP_HIT** — E10 (Mypy 1.17 Released 2025-07-14). AMBER: johal.in mypy strict article (no date).
- **Pydantic V2 (E3):** Not added; E3 already dated OK; no 2025-06+ source was required for this run.

**Total TOP_HITs:** 5 (E6, E6b, E7, E8, E10; E9 is AMBER). **AMBERs remaining:** 3 (two johal.in pages without dates, one structlog 25.3.0 doc before 2025-06-01).

*Web Scout run: 2026-03-03. Evidence Schema: EN-only, published/updated_date ≥ 2025-06-01 for TOP_HIT.*

---

이 보고서는 **제안·계획 문서**이며, 자동 코드 변경/커밋/배포는 하지 않습니다. 적용 시 Agent 모드에서 단계별로 진행하시면 됩니다.