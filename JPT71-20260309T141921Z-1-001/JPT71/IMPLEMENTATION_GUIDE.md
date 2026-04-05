# Excel to Python 구현 가이드

이 문서는 `excel_python_engine.py`를 사용하여 Excel 파일을 Python으로 구현하는 방법을 설명합니다.

## 목차

1. [개요](#개요)
2. [아키텍처](#아키텍처)
3. [사용 방법](#사용-방법)
4. [클래스 설명](#클래스-설명)
5. [Excel 함수 지원](#excel-함수-지원)
6. [고급 기능](#고급-기능)

---

## 개요

`excel_python_engine.py`는 Excel 파일을 완전히 Python으로 구현하기 위한 엔진입니다. 다음 기능을 제공합니다:

- ✅ Excel 파일 로드 및 저장
- ✅ 셀 참조 처리 (A1, $B$2, Sheet!A1 등)
- ✅ Excel 함수 계산 (INDEX, ROW, IFERROR, IF, SMALL, VLOOKUP 등)
- ✅ 의존성 그래프 기반 계산 순서 결정
- ✅ 순환 참조 감지
- ✅ 포맷/스타일 재현 (폰트, 색상, 정렬, 숫자 포맷)

---

## 아키텍처

### 클래스 구조

```
ExcelWorkbook
├── ExcelSheet (여러 개)
│   └── ExcelCell (여러 개)
├── FormulaEngine
│   └── Excel 함수 구현들
└── StyleEngine
```

### 주요 클래스

1. **ExcelWorkbook**: 전체 워크북 관리
2. **ExcelSheet**: 시트 데이터 및 구조
3. **ExcelCell**: 개별 셀 데이터 및 포맷
4. **CellReference**: 셀 참조 파싱 및 처리
5. **FormulaEngine**: Excel 함수 계산 엔진
6. **StyleEngine**: 포맷/스타일 적용

---

## 사용 방법

### 기본 사용

```python
from excel_python_engine import ExcelWorkbook

# 1. Excel 파일 로드
workbook = ExcelWorkbook.load_from_excel("content-calendar.xlsx")

# 2. 함수 계산
workbook.calculate_all()

# 3. 결과 확인
sheet = workbook.get_sheet("Content")
cell = sheet.get_cell("A1")
print(f"Value: {cell.get_value()}")

# 4. Excel 파일로 저장
workbook.save_to_excel("output.xlsx")
```

### 명령줄 사용

```bash
python excel_python_engine.py content-calendar.xlsx output.xlsx
```

### 테스트 실행

```bash
python test_excel_engine.py
```

---

## 클래스 설명

### ExcelWorkbook

전체 Excel 워크북을 관리하는 메인 클래스입니다.

**주요 메서드:**

- `load_from_excel(excel_path: str) -> ExcelWorkbook`: Excel 파일 로드
- `save_to_excel(output_path: str)`: Excel 파일로 저장
- `get_sheet(name: str) -> Optional[ExcelSheet]`: 시트 가져오기
- `add_sheet(sheet: ExcelSheet)`: 시트 추가
- `calculate_all()`: 모든 함수 계산

**예제:**

```python
workbook = ExcelWorkbook.load_from_excel("file.xlsx")
workbook.calculate_all()
workbook.save_to_excel("output.xlsx")
```

### ExcelSheet

Excel 시트를 나타내는 클래스입니다.

**주요 속성:**

- `name`: 시트 이름
- `rows`: 행 수
- `cols`: 열 수
- `cells`: 셀 딕셔너리 (coordinate -> ExcelCell)
- `column_widths`: 열 너비
- `row_heights`: 행 높이
- `merged_cells`: 병합된 셀 목록

**주요 메서드:**

- `get_cell(coordinate: str) -> Optional[ExcelCell]`: 셀 가져오기
- `set_cell(coordinate: str, cell: ExcelCell)`: 셀 설정
- `get_cell_value(coordinate: str) -> Any`: 셀 값 가져오기

**예제:**

```python
sheet = workbook.get_sheet("Content")
cell = sheet.get_cell("A1")
value = sheet.get_cell_value("A1")
```

### ExcelCell

개별 셀의 데이터와 포맷을 저장하는 클래스입니다.

**주요 속성:**

- `coordinate`: 셀 좌표 (예: "A1")
- `value`: 셀 값
- `formula`: 함수 문자열 (예: "=A1+B1")
- `data_type`: 셀 타입 (VALUE, FORMULA, EMPTY)
- `calculated_value`: 계산된 값
- `font`, `fill`, `alignment`, `border`, `number_format`: 포맷 정보

**예제:**

```python
cell = ExcelCell(
    coordinate="A1",
    value=10,
    data_type=CellType.VALUE
)
```

### CellReference

셀 참조를 파싱하고 처리하는 클래스입니다.

**지원하는 형식:**

- `A1`: 상대 참조
- `$A$1`: 절대 참조
- `$A1`: 절대 열, 상대 행
- `A$1`: 상대 열, 절대 행
- `Sheet1!A1`: 다른 시트 참조
- `Sheet1!$A$1`: 다른 시트 절대 참조

**주요 메서드:**

- `parse(ref: str, current_sheet: str = None) -> CellReference`: 셀 참조 파싱
- `to_string() -> str`: 문자열로 변환
- `resolve(base_sheet, base_row, base_col) -> Tuple`: 상대 참조를 절대 좌표로 변환

**예제:**

```python
ref = CellReference.parse("Sheet1!$A$1")
print(ref.sheet)  # "Sheet1"
print(ref.column)  # "A"
print(ref.row)  # 1
print(ref.absolute_column)  # True
print(ref.absolute_row)  # True
```

### FormulaEngine

Excel 함수를 계산하는 엔진입니다.

**지원하는 함수:**

- `IF`, `IFERROR`
- `INDEX`, `ROW`, `SMALL`
- `VLOOKUP`
- `HYPERLINK`, `SUBSTITUTE`
- `DATE`, `WEEKDAY`
- `UPPER`, `TEXT`
- `COUNTIF`, `TEXTJOIN`, `OFFSET`

**주요 메서드:**

- `evaluate(formula: str, sheet_name: str, cell_coord: str) -> Any`: 함수 평가

**예제:**

```python
engine = FormulaEngine(workbook)
result = engine.evaluate("=IF(A1>5, \"Yes\", \"No\")", "Sheet1", "B1")
```

---

## Excel 함수 지원

### 구현된 함수 목록

| Excel 함수 | Python 구현 | 설명 |
|-----------|------------|------|
| `IF` | `_excel_if` | 조건부 반환 |
| `IFERROR` | `_excel_iferror` | 에러 처리 |
| `INDEX` | `_excel_index` | 배열 인덱싱 |
| `ROW` | `_excel_row` | 행 번호 반환 |
| `SMALL` | `_excel_small` | k번째 작은 값 |
| `VLOOKUP` | `_excel_vlookup` | 수직 조회 |
| `HYPERLINK` | `_excel_hyperlink` | 하이퍼링크 |
| `SUBSTITUTE` | `_excel_substitute` | 문자열 치환 |
| `DATE` | `_excel_date` | 날짜 생성 |
| `WEEKDAY` | `_excel_weekday` | 요일 반환 |
| `UPPER` | `_excel_upper` | 대문자 변환 |
| `TEXT` | `_excel_text` | 텍스트 포맷팅 |
| `COUNTIF` | `_excel_countif` | 조건부 카운트 |
| `TEXTJOIN` | `_excel_textjoin` | 텍스트 결합 |
| `OFFSET` | `_excel_offset` | 오프셋 참조 |

### 함수 사용 예제

```python
# IF 함수
=IF(A1>10, "High", "Low")

# VLOOKUP 함수
=VLOOKUP(A1, Table1!A:B, 2, FALSE)

# INDEX 함수
=INDEX(A1:C10, 3, 2)

# IFERROR 함수
=IFERROR(A1/B1, 0)

# DATE 함수
=DATE(2025, 12, 30)

# COUNTIF 함수
=COUNTIF(A1:A10, ">5")
```

---

## 고급 기능

### 의존성 그래프

함수 간 의존성을 분석하여 올바른 계산 순서를 결정합니다.

```python
# 의존성 그래프 생성
graph = workbook._build_dependency_graph()

# 계산 순서 결정 (위상 정렬)
order = workbook._topological_sort(graph)
```

### 순환 참조 감지

순환 참조가 있는 경우 경고를 표시하고 가능한 한 계산을 진행합니다.

```python
# 순환 참조가 있으면 remaining에 포함됨
remaining = all_nodes - visited
if remaining:
    print(f"순환 참조 감지: {remaining}")
```

### 포맷 재현

셀의 포맷 정보를 Excel 파일로 저장할 때 재현합니다.

```python
# 포맷 정보가 있는 셀
cell = ExcelCell(
    coordinate="A1",
    value="Hello",
    font={'name': 'Arial', 'size': 12, 'bold': True},
    fill={'patternType': 'solid', 'fgColor': 'FFFF00'},
    alignment={'horizontal': 'center', 'vertical': 'middle'}
)
```

### 커스텀 함수 추가

새로운 Excel 함수를 추가하려면 `FormulaEngine._register_functions()`를 확장하세요.

```python
def _excel_custom(self, args: List[Any], sheet_name: str, cell_coord: str) -> Any:
    """커스텀 함수 구현"""
    # 함수 로직
    return result

# 등록
self.function_registry['CUSTOM'] = self._excel_custom
```

---

## 제한사항

1. **복잡한 배열 함수**: 일부 배열 함수는 제한적으로 지원됩니다.
2. **매크로**: VBA 매크로는 지원하지 않습니다.
3. **차트/그래프**: 차트 객체는 지원하지 않습니다.
4. **조건부 포맷팅**: 일부 고급 조건부 포맷팅은 제한적입니다.

---

## 문제 해결

### 함수 계산 오류

함수 계산이 실패하는 경우:

1. 셀 참조가 올바른지 확인
2. 함수 인자가 올바른지 확인
3. 의존하는 셀의 값이 계산되었는지 확인

### 순환 참조

순환 참조가 발생하는 경우:

1. 의존성 그래프를 확인
2. 순환 참조를 제거하거나 수정
3. 반복 계산으로 해결 (향후 구현 예정)

---

## 참고 자료

- [가이드 문서](content-calendar.guide.md): Excel 파일 구조 분석
- [테스트 스크립트](test_excel_engine.py): 사용 예제 및 테스트
- [원본 엔진](excel_python_engine.py): 전체 구현 코드

---

## 라이선스

이 프로젝트는 내부 사용을 위한 것입니다.

