import streamlit as st
import plotly.express as px
import pandas as pd

def show_shelter_analysis(filtered_df):
    """보호소 분석 페이지를 표시합니다."""
    st.title("보호소 분석")
    
    # 보호소별 유기동물 수
    st.header("보호소별 유기동물 수")
    if 'care_nm' in filtered_df.columns:
        # 상위 10개 보호소
        shelter_counts = filtered_df['care_nm'].value_counts().head(10).reset_index()
        shelter_counts.columns = ['shelter', 'count']
        
        fig = px.bar(shelter_counts, x='shelter', y='count',
                     title="상위 10개 보호소 유기동물 수",
                     color='shelter',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
        
        # 보호소별 입양률
        if 'process_state' in filtered_df.columns:
            st.header("보호소별 입양률 (상위 10개)")
            
            # 보호소별 총 동물 수와 입양 동물 수 계산
            shelter_adoption = filtered_df.groupby('care_nm').apply(
                lambda x: pd.Series({
                    'total': len(x),
                    'adopted': len(x[x['process_state'] == '입양'])
                })
            ).reset_index()
            
            # 입양률 계산
            shelter_adoption['adoption_rate'] = shelter_adoption['adopted'] / shelter_adoption['total'] * 100
            
            # 총 동물 수가 일정 수 이상인 보호소만 선택 (통계적 의미를 위해)
            min_animals = 20  # 최소 20마리 이상 보호한 보호소만 고려
            significant_shelters = shelter_adoption[shelter_adoption['total'] >= min_animals]
            
            # 입양률 기준 상위 10개 보호소
            top_shelters = significant_shelters.sort_values('adoption_rate', ascending=False).head(10)
            
            fig = px.bar(top_shelters, x='care_nm', y='adoption_rate',
                        title=f"보호소별 입양률 (최소 {min_animals}마리 이상 보호)",
                        color='care_nm',
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(xaxis_title="보호소", yaxis_title="입양률 (%)")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("보호소 정보가 데이터에 없습니다.")
    
    # 지역별 보호소 분포
    st.header("지역별 보호소 분포")
    if 'care_nm' in filtered_df.columns and 'sido' in filtered_df.columns:
        # 시도별 보호소 수 계산
        sido_shelter_counts = filtered_df.groupby('sido')['care_nm'].nunique().reset_index()
        sido_shelter_counts.columns = ['sido', 'shelter_count']
        
        # 시도별 보호소당 평균 동물 수 계산
        sido_animal_counts = filtered_df.groupby('sido').size().reset_index(name='animal_count')
        
        # 데이터 병합
        sido_analysis = pd.merge(sido_shelter_counts, sido_animal_counts, on='sido')
        sido_analysis['animals_per_shelter'] = sido_analysis['animal_count'] / sido_analysis['shelter_count']
        
        # 보호소 수 그래프
        fig = px.bar(sido_shelter_counts, x='sido', y='shelter_count',
                    title="지역별 보호소 수",
                    color='sido',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
        
        # 보호소당 평균 동물 수 그래프
        fig = px.bar(sido_analysis, x='sido', y='animals_per_shelter',
                    title="지역별 보호소당 평균 동물 수",
                    color='sido',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("보호소 또는 지역 정보가 데이터에 없습니다.")