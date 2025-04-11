# animal-forest

dashboard/
├── main.py                     # 메인 Streamlit 앱 (진입점)
├── data_loader.py              # 데이터 로딩 기능
├── data_processor.py           # 데이터 전처리 기능
├── utils.py                    # 유틸리티 함수들
├── page_modules/               # 페이지 모듈 디렉토리
│   ├── __init__.py             # 페이지 패키지 초기화 파일
│   ├── main_dashboard.py       # 메인 대시보드 페이지
│   ├── animal_traits.py        # 동물 특성 분석 페이지
│   ├── location_analysis.py    # 지역 및 발견 장소 분석 페이지
│   ├── time_pattern.py         # 시간 패턴 분석 페이지
│   ├── survival_factors.py     # 생존 요인 분석 페이지
│   ├── shelter_analysis.py     # 보호소 분석 페이지
│   └── data_table.py           # 데이터 테이블 페이지
├── requirements.txt            # 필요 패키지 목록
└── data/                       # 데이터 파일 디렉토리
    └── abandonment_public.csv  # 기본 데이터 파일
    └── korea_geojson  # 지역별 geojson파일 디렉토리


## 주요 기능

