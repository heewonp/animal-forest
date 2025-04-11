import streamlit as st
import os
from utils.data_loader import DataLoader
from utils.data_processor import AnimalDataProcessor

# 페이지 모듈 import
from page_modules.main_dashboard import show_main_dashboard
from page_modules.animal_traits import show_animal_traits
from page_modules.location_analysis import show_location_analysis
from page_modules.time_pattern import show_time_pattern
from page_modules.survival_factors import show_survival_factors
from page_modules.shelter_analysis import show_shelter_analysis
from page_modules.data_table import show_data_table

# 페이지 설정
st.set_page_config(
    page_title="유기동물 데이터 분석 대시보드",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 관리
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# data 폴더에서 CSV 파일 불러오기
def load_data_from_file(file_name):
    try: 
        # data 폴더 내의 파일 경로 생성
        file_path = os.path.join('data', file_name)
        
        # DataLoader를 사용해 파일 로드
        df = DataLoader.load_from_file(file_path)
        
        if df is not None:
            # 데이터 전처리
            processor = AnimalDataProcessor(df)  
            processed_df = processor.preprocess_data()
            
            # 세션 상태에 저장
            st.session_state.processed_data = processed_df
            return True
            
        return False
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return False

# 기본 데이터 파일 로드
default_file = 'abandonment_public.csv'  # 파일명만 지정

# 앱 시작시 기본 데이터 로드 시도
if st.session_state.processed_data is None:
    if load_data_from_file(default_file):
        st.sidebar.success(f"{default_file} 데이터가 로드되었습니다.")
    else:
        st.sidebar.warning(f"{default_file} 데이터를 로드할 수 없습니다.")

# 사이드바 메뉴
st.sidebar.title("유기동물 데이터 분석")
menu = st.sidebar.radio(
    "메뉴 선택",
    ["메인 대시보드", "동물 특성 분석", "지역 및 발견 장소 분석", "시간 패턴 분석", "생존 요인 분석", "보호소 분석", "데이터 테이블"]
)

# 파일 업로드 옵션
uploaded_file = st.sidebar.file_uploader("CSV 파일 업로드", type=['csv'])

if uploaded_file is not None:
    try:
        # 업로드된 파일 로드
        df = DataLoader.load_from_uploaded_file(uploaded_file)
        
        if df is not None:
            # 데이터 전처리
            processor = AnimalDataProcessor(df)
            processed_df = processor.preprocess_data()
            
            # 세션 상태에 저장
            st.session_state.processed_data = processed_df
            st.sidebar.success(f"{uploaded_file.name} 데이터가 성공적으로 처리되었습니다.")
        else:
            st.sidebar.error("데이터를 로드할 수 없습니다.")
    except Exception as e:
        st.sidebar.error(f"데이터 처리 중 오류 발생: {e}")

# 필터링된 데이터 가져오기
filtered_df = st.session_state.processed_data

# 페이지 라우팅
if filtered_df is not None:
    if menu == "메인 대시보드":
        show_main_dashboard(filtered_df)
    elif menu == "동물 특성 분석":
        show_animal_traits(filtered_df)
    elif menu == "지역 및 발견 장소 분석":
        show_location_analysis(filtered_df)
    elif menu == "시간 패턴 분석":
        show_time_pattern(filtered_df)
    elif menu == "생존 요인 분석":
        show_survival_factors(filtered_df)
    elif menu == "보호소 분석":
        show_shelter_analysis(filtered_df)
    elif menu == "데이터 테이블":
        show_data_table(filtered_df)
else:
    st.warning("데이터가 로드되지 않았습니다. 사이드바에서 파일을 업로드하거나 기본 데이터가 로드될 때까지 기다려주세요.")