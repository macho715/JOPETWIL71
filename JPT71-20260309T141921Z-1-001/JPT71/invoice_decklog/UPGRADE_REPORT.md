# UPGRADE_REPORT — JPT71/invoice_decklog

**Scope anchor**: 본 보고서의 범위는 [JPT71 종합 리포트.md](JPT71%20종합%20리포트.md)에 정리된 구현 범위(plan §1~5, §11, Option C)를 기준으로 합니다.  
Evidence 및 Best3는 기존 [upgrade.md](upgrade.md) 및 [upgrade_evidence_section.md](upgrade_evidence_section.md)의 2025-06+ TOP_HIT와 정합합니다.

---

## 1. Executive Summary

- **범위**: `JPT71/invoice_decklog` — OFCO·decklog·jpt71 엑셀 기반 운영 보고서 + Data Spine(Scorecard, Leakage, Exception, Dual_Value, Manifest). 종합 리포트 기준으로 기준키 정규화, TagMap v1.1, 4산출물·옵션 갭(Dual-Value, Charter/CostType, DATA_CONTRACT)이 구현 완료 상태.
- **현재 상태**: Python 3.11+, pandas + openpyxl, YAML 설정, 타입 힌트 일부 사용. **테스트/CI 없음**, **구조화 로깅 없음**, requirements.txt 없음.
- **제안**: 신뢰성(테스트·검증)·관찰성(로깅)·설정·DX·문서화 5개 버킷에서 Top10 아이디어 유지, Best3 Deep(테스트·로깅·Excel 계약 강화) 적용 권장. Evidence는 2025-06+ EN 자료(TOP_HIT)로 보강 완료.

---

## 2. Current State Snapshot (Doc-first)

| 항목 | 내용 |
|------|------|
| **범위 기준** | JPT71 종합 리포트.md (plan §1~5, §11, Option C 구현 완료) |
| **진입점** | `jpt71_ops_report.py` (argparse, `main()` → MD/Excel), `jpt71_spine.py` (run_spine) |
| **입력** | ofco detail.xlsx (OFCO INVOICE ALL), decklog.xlsx (첫 시트), jpt71.xlsx (Sheet2), INVOICE.xlsx (선택), TagMap_v1.1.csv, config_jpt71_report.yml |
| **출력** | out/JPT71_ops_report.md, out/JPT71_ops_summary.xlsx (By_Voyage, PriceCenter_Detail, Voyage_Scorecard, Leakage_Ledger, Exception_Ledger, InvoiceKey_Collision, bridge_voyage_month, Dual_Value), out/run_manifest.json |
| **의존성** | pandas, openpyxl, PyYAML (spine); requirements.txt 없음 |
| **테스트** | 없음 (pytest/test_* 미사용) |
| **CI** | 없음 |
| **로깅** | print() 위주, 구조화 로깅/JSON 로그 없음 |
| **설정** | config_jpt71_report.yml (config_version 1.0), dict 기반, Pydantic 미사용 |
| **타입** | 함수 시그니처 타입 힌트 일부, mypy/strict 미적용 |
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
| 배포/실행 | CLI 로컬 실행 |
| 제약 | 엑셀 시트/컬럼 계약(DATA_CONTRACT), OFCO/jpt71/decklog 파일명·시트명 고정 가정 |

---

## 4. Upgrade Ideas Top 10 (6 buckets)

| # | Bucket | Idea | PriorityScore | Evidence |
|---|--------|------|---------------|----------|
| 1 | Reliability | Excel 로더에 fixture 기반 pytest 추가 (필수 컬럼·dtype·샘플 시트) | 높음 | E6, E7 |
| 2 | Reliability | read_excel에 sheet_name/header/usecols/dtype 명시 및 DATA_CONTRACT와 정렬 | 높음 | E6/E6b, DATA_CONTRACT.md |
| 3 | Security | 설정/비밀: .env + pydantic-settings, 비밀 로그 금지 | 중간 | E3, 보안 관행 |
| 4 | Performance | 대용량 decklog/OFCO 시 nrows/usecols 또는 1회 Parquet 스테이징 검토 | 중간 | E6 |
| 5 | DX | mypy --strict 단계 도입 (신규/수정 모듈부터) | 중간 | E10 |
| 6 | DX | Pydantic 모델로 config 로드 (config_version, tagmap, mismatch, charter 등) | 높음 | E3 |
| 7 | Architecture | 로더/집계/쓰기 책임 분리 (read/validate → business logic → write) | 중간 | E6 |
| 8 | Docs | DATA_CONTRACT에 "필수 컬럼 집합" 및 실패 시 동작 명시, run_manifest 필드 설명 보강 | 낮음 | 현행 문서 |
| 9 | Reliability | run 시 품질 지표 로깅 (rows_read, unknown_rate, unmatched_count, null 핵심 컬럼 수) | 높음 | E6, E8 |
| 10 | DX | structlog 도입(JSON + console), 실행 요약·실패 시 traceback 구조화 로깅 | 높음 | E8 |

---

## 5. Best 3 Deep Report

### Best #1: Fixture 기반 pytest로 Excel/Spine 계약 검증

- **Goal**: 엑셀 입력·스파인 출력에 대한 회귀 방지 및 계약 안정화.
- **Design**: `tests/` 하위에 `test_load_ofco.py`, `test_spine_integration.py` 등; 소형 fixture 엑셀(필수 컬럼만)·기대 시트/행 수/키 유니크; DATA_CONTRACT 필수 컬럼 assert.
- **PR Plan**: (1) tests/ + conftest.py 및 fixture 엑셀 추가, (2) load_ofco_detail / load_decklog 필수 컬럼 검증 테스트, (3) run_spine 스모크(고정 fixture → Scorecard/Leakage 행 수·컬럼 존재).
- **Tests**: 필수 컬럼 누락 시 ValueError, 동일 fixture에서 Scorecard 합계 불변.
- **Rollout/Rollback**: 로컬만 기본; CI 연동 시 해당 job 비활성화로 롤백.
- **Risks**: fixture가 실제 파일과 어긋나면 false positive → DATA_CONTRACT와 동기화 의무.
- **KPIs**: 커밋 전 pytest 통과, spine 변경 시 관련 테스트 1개 이상.
- **Evidence**: E6, E7 (pandas 2.3.1/3.0.1 read_excel, pytest-regressions 2.8.1 2025-07-04).

### Best #2: structlog + 실행 요약/품질 지표 로깅

- **Goal**: 배치 실패·품질 저하를 3AM에도 추적 가능하게.
- **Design**: structlog 설정(JSON 파일/콘솔), `jpt71_ops_report.py`/`jpt71_spine.py`에서 print 대신 logger; run 종료 시 rows_read, unknown_rate, unmatched_count, collision_count, outputs, run_id 등 구조화 로그 1건.
- **PR Plan**: (1) structlog 의존성 및 logger 설정 모듈, (2) main/run_spine에 로그 호출 추가, (3) run_manifest와 동일 메타를 로그에 출력.
- **Tests**: 로그 캡처 후 "run_id" 또는 "unknown_rate" 키 존재 assert.
- **Rollout/Rollback**: 로그 레벨/타겟만 변경으로 롤백 용이.
- **Risks**: 로그에 민감 필드 포함 금지.
- **KPIs**: 매 run 구조화 로그 1건, 실패 시 traceback 로그.
- **Evidence**: E8 (structlog 25.4.0 2025-06-02).

### Best #3: Excel read 계약 명시 + DATA_CONTRACT 정렬

- **Goal**: read_excel을 "계약 경계"로 두고, 시트/헤더/컬럼/타입을 문서와 코드에서 일치.
- **Design**: 모든 read_excel에 sheet_name, header(또는 skiprows), usecols 또는 EXPECTED_COLUMNS 기반 검증; DATA_CONTRACT.md에 "Input sheets" 테이블 추가(시트명·필수 컬럼·타입).
- **PR Plan**: (1) DATA_CONTRACT에 입력 시트·필수 컬럼 명시, (2) load_ofco_detail/load_decklog/load_jpt71_sheet2_with_keys에 필수 컬럼 검증 및 명시적 read_excel 인자, (3) 누락 시 ValueError 메시지에 누락 컬럼명 포함.
- **Tests**: 필수 컬럼 누락 fixture로 ValueError 발생 테스트.
- **Rollout/Rollback**: 기존 파일이 계약 만족 시 동작 동일; 불만족 시 의도적 실패.
- **Risks**: 기존 엑셀에 선택 컬럼 없으면 즉시 실패 → 운영팀에 계약 공유 필요.
- **KPIs**: 계약 위반 시 1회 run 내 실패, 문서와 코드 일치.
- **Evidence**: E6, E6b, DATA_CONTRACT.md.

---

## 6. Options & Roadmap

- **Option A (최소)**: Best #3만 적용 — 계약 명시 + read_excel 정리.
- **Option B (권장)**: Best #1 + #3 → 테스트 + 계약.
- **Option C (전체)**: Best #1 + #2 + #3 → 테스트 + 로깅 + 계약.

**30/60/90-day Roadmap**

| 기간 | 권장 작업 |
|------|-----------|
| 30일 | DATA_CONTRACT 입력 명세, read_excel 명시화, Best #3 적용 |
| 60일 | tests/ 추가, fixture 및 Best #1 적용 |
| 90일 | structlog 도입 및 실행 요약 로깅(Best #2), (선택) CI에서 pytest 실행 |

---

## 7. Evidence Table (2025-06+ TOP_HIT)

| ID | URL/소스 | published/updated | 비고 |
|----|----------|-------------------|------|
| E3 | pydantic.com (V2 config) | 2025+ | OK |
| E6 | pandas 2.3.1 What's new | 2025-07-07 | TOP_HIT |
| E6b | pandas.read_excel API (3.0.1 docs) | 2026-02-17 | TOP_HIT |
| E7 | pytest-regressions 2.8.1 (PyPI) | 2025-07-04 | TOP_HIT |
| E8 | structlog 25.4.0 Release | 2025-06-02 | TOP_HIT |
| E10 | Mypy 1.17 Released | 2025-07-14 | TOP_HIT |

상세 URL·제목·relevance는 [upgrade_evidence_section.md](upgrade_evidence_section.md) 참조.

---

## 8. AMBER_BUCKET

- 원문에 published_date 없는 소스(E1, E2, E4, E5 원본)는 본 회차에서 E6, E6b, E7, E8, E10으로 대체·보강됨.
- johal.in 등 날짜 미명시 자료는 TOP_HIT 채택 제외, 참고용으로만 활용.

---

## 9. Open Questions (≤3)

1. **CI**: pytest를 GitHub Actions 등에서 실행할지, fixture 엑셀을 레포에 포함할지 여부.
2. **의존성 고정**: requirements.txt 또는 pyproject.toml에 pandas/openpyxl 버전 고정 및 "ingestion smoke test in CI" 도입 여부.
3. **PDF 인보이스**: 첨부 Invoice PDF는 현재 파이프라인 미연동; 추후 OCR/추출 연동 시 보안·감사 로깅 요구사항 정리 필요.

---

*본 보고서는 제안·계획 문서이며, 자동 코드 변경/커밋/배포는 하지 않습니다. 적용 시 Agent 모드에서 단계별 진행.*
