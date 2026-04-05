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

**Total TOP_HITs:** 6 (E6, E6b, E7, E8, E10; E9 is AMBER). **AMBERs remaining:** 3 (two johal.in pages without dates, one structlog 25.3.0 doc before 2025-06-01).

---

*Accessed: 2026-03-03. Do not modify code or repo; paste this section into upgrade.md as needed.*
