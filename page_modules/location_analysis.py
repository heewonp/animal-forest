import streamlit as st
import plotly.express as px
import pandas as pd

def show_location_analysis(filtered_df):
    """지역 및 발견 장소 분석 페이지를 표시합니다."""
    st.title("지역 및 발견 장소 분석")
    
    # 지역별 유기동물 발생 현황
    st.header("지역별 유기동물 발생 현황")
    if 'sido' in filtered_df.columns:
        # 시도별 발생 건수
        sido_counts = filtered_df['sido'].value_counts().reset_index()
        sido_counts.columns = ['sido', 'count']
        
        fig = px.bar(sido_counts, x='sido', y='count', 
                    title="시도별 유기동물 발생 건수",
                    color='sido',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
        
        # 권역별 발생 건수
        if 'region' in filtered_df.columns:
            region_counts = filtered_df['region'].value_counts().reset_index()
            region_counts.columns = ['region', 'count']
            
            fig = px.pie(region_counts, values='count', names='region', 
                        title="권역별 유기동물 발생 비율",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
    
    # 발견 장소 유형 분석
    st.header("발견 장소 유형 분석")
    if 'place_type' in filtered_df.columns:
        place_type_counts = filtered_df['place_type'].value_counts().reset_index()
        place_type_counts.columns = ['place_type', 'count']
        
        fig = px.bar(place_type_counts, x='place_type', y='count', 
                    title="장소 유형별 발생 건수",
                    color='place_type',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    # 시설 특성별 분석
    st.header("시설 특성별 분석")
    if 'facility_types' in filtered_df.columns:
        # 시설 특성을 개별 항목으로 분리하여 빈도 계산
        facility_list = []
        for facilities in filtered_df['facility_types']:
            for facility in facilities.split(', '):
                facility_list.append(facility)
        
        facility_counts = pd.Series(facility_list).value_counts().reset_index()
        facility_counts.columns = ['facility', 'count']
        
        # 상위 10개 시설만 표시
        facility_counts = facility_counts.head(10)
        
        fig = px.bar(facility_counts, x='facility', y='count', 
                    title="상위 10개 시설 특성",
                    color='facility',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    # 지역별 동물 유형 분포
    st.header("지역별 동물 유형 분포")
    if 'sido' in filtered_df.columns and 'animal_type' in filtered_df.columns:
        # 상위 5개 시도만 선택
        top_sidos = filtered_df['sido'].value_counts().head(5).index.tolist()
        
        # 시도별, 동물 유형별 집계
        cross_tab = pd.crosstab(
            filtered_df[filtered_df['sido'].isin(top_sidos)]['sido'], 
            filtered_df[filtered_df['sido'].isin(top_sidos)]['animal_type']
        ).reset_index()
        
        # Melt 데이터프레임으로 변환
        melted_df = pd.melt(cross_tab, id_vars=['sido'], var_name='animal_type', value_name='count')
        
        fig = px.bar(melted_df, x='sido', y='count', color='animal_type',
                     title="상위 5개 시도별 동물 유형 분포",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)