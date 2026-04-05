# Content Calendar Python Application

Excel 파일(`content-calendar.xlsx`)을 완전한 Python 애플리케이션으로 변환한 구현입니다.

## 파일 구조

```
JPT71/
├── excel_python_engine.py      # Excel 엔진 (함수 계산, 셀 참조 처리)
├── content_calendar_app.py     # Content Calendar 애플리케이션
├── run_excel_engine.py         # Excel 엔진 실행 스크립트
├── test_excel_engine.py        # 테스트 스크립트
├── IMPLEMENTATION_GUIDE.md      # 구현 가이드
└── content-calendar.guide.md   # Excel 구조 분석 가이드
```

## 사용 방법

### 1. 기본 실행

```bash
python content_calendar_app.py [excel_file_path]
```

### 2. Excel 파일에서 데이터 로드

```python
from content_calendar_app import ContentCalendarApplication

app = ContentCalendarApplication()
app.load_from_excel("content-calendar_calculated.xlsx")

# 캘린더 뷰 생성
calendar_view = app.get_calendar_view()

# JSON으로 내보내기
app.export_to_json("output.json")

# HTML로 내보내기
app.export_to_html("output.html")
```

### 3. 프로그래밍 방식으로 데이터 추가

```python
from content_calendar_app import ContentCalendarApplication, ContentItem
from datetime import date

app = ContentCalendarApplication()

# 콘텐츠 항목 추가
item = ContentItem(
    id="1",
    title="새 콘텐츠",
    description="설명",
    date=date(2025, 12, 30),
    status="Draft",
    hashtags=["#marketing", "#social"]
)
app.add_content_item(item)

# 캘린더 뷰 생성 및 내보내기
app.export_to_html("calendar.html")
```

## 주요 클래스

### ContentCalendarApplication

메인 애플리케이션 클래스

**주요 메서드:**
- `load_from_excel(excel_path)`: Excel 파일에서 데이터 로드
- `get_calendar_view()`: 캘린더 뷰 생성
- `add_content_item(item)`: 콘텐츠 항목 추가
- `export_to_json(output_path)`: JSON으로 내보내기
- `export_to_html(output_path)`: HTML로 내보내기
- `print_summary()`: 요약 정보 출력

### CalendarCalculator

캘린더 계산 로직 (Excel 함수를 Python으로 변환)

**주요 메서드:**
- `get_first_day_of_month(year, month)`: 월의 첫 번째 날짜
- `get_weekday(date_val, return_type)`: 요일 반환
- `get_calendar_start_date(base_date, start_day)`: 캘린더 시작 날짜 계산
- `generate_calendar_dates(start_date, weeks)`: 캘린더 날짜 목록 생성

### ContentRepository

콘텐츠 데이터 저장소

**주요 메서드:**
- `add_item(item)`: 콘텐츠 항목 추가
- `get_items_for_date(target_date)`: 특정 날짜의 콘텐츠 조회
- `get_items_for_range(start_date, end_date)`: 날짜 범위의 콘텐츠 조회

### CalendarView

캘린더 뷰 생성

**주요 메서드:**
- `generate_month_view(year, month, start_day)`: 월별 캘린더 뷰 생성

## Excel 함수 매핑

| Excel 함수 | Python 구현 |
|-----------|------------|
| `DATE` | `CalendarCalculator.get_first_day_of_month()` |
| `WEEKDAY` | `CalendarCalculator.get_weekday()` |
| `VLOOKUP` | `ContentRepository.get_items_for_date()` |
| `IF` | Python `if/else` |
| `IFERROR` | Python `try/except` |

## 출력 형식

### JSON 출력

```json
{
  "year": 2025,
  "month": 12,
  "month_name": "DECEMBER 2025",
  "start_date": "2025-11-30",
  "weeks": [
    [
      {
        "date": "2025-11-30",
        "day": 30,
        "is_current_month": false,
        "is_today": false,
        "weekday": "Sunday",
        "items": [...],
        "item_count": 0
      },
      ...
    ],
    ...
  ],
  "settings": {...},
  "all_content_items": [...]
}
```

### HTML 출력

반응형 HTML 캘린더 뷰가 생성됩니다:
- 월별 그리드 레이아웃
- 날짜별 콘텐츠 표시
- 오늘 날짜 하이라이트
- 다른 월 날짜 회색 표시

## 개선 사항

현재 구현된 기능:
- ✅ Excel 파일 로드
- ✅ 캘린더 계산 로직
- ✅ 콘텐츠 데이터 관리
- ✅ JSON/HTML 내보내기

추가 개선 가능 사항:
- [ ] Excel의 정확한 컬럼 매핑 분석 및 적용
- [ ] 날짜 파싱 개선 (Excel 날짜 형식 처리)
- [ ] 더 많은 Excel 함수 지원
- [ ] 데이터베이스 연동
- [ ] 웹 인터페이스 추가
- [ ] API 엔드포인트 제공

## 의존성

- `excel_python_engine.py` (필수)
- `openpyxl` (Excel 파일 읽기/쓰기)
- Python 3.7+

## 라이선스

내부 사용 목적

