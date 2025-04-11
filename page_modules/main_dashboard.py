import streamlit as st
import plotly.express as px

def show_main_dashboard(filtered_df):
    """메인 대시보드 페이지를 표시합니다."""
    st.title("유기동물 데이터 분석 대시보드")
    st.markdown("### 유기동물 현황 종합")
    
    # 카드 형태의 주요 통계 정보
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 유기동물 수", f"{len(filtered_df):,}마리")
    
    if 'process_state' in filtered_df.columns:
        status_counts = filtered_df['process_state'].value_counts()
        
        with col2:
            adopted_count = status_counts.get('입양', 0) + status_counts.get('종료(입양)', 0)
            st.metric("입양된 동물", f"{adopted_count:,}마리")
        
        with col3:
            protecting_count = status_counts.get('보호중', 0)
            st.metric("보호중인 동물", f"{protecting_count:,}마리")
        
        with col4:
            death_count = status_counts.get('자연사', 0) + status_counts.get('종료(자연사)', 0) + status_counts.get('안락사', 0) + status_counts.get('종료(안락사)', 0)
            st.metric("사망한 동물", f"{death_count:,}마리")
    
    st.markdown("---")
    
    # 동물 종류별 분포
    if 'animal_type' in filtered_df.columns:
        st.subheader("동물 종류별 분포")
        animal_type_counts = filtered_df['animal_type'].value_counts().reset_index()
        animal_type_counts.columns = ['animal_type', 'count']
        
        fig = px.pie(animal_type_counts, values='count', names='animal_type', 
                     title="동물 종류별 분포",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    # 상태별 분포
    if 'process_state' in filtered_df.columns:
        st.subheader("동물 상태별 분포")
        status_counts = filtered_df['process_state'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        
        fig = px.bar(status_counts, x='status', y='count', 
                    title="상태별 유기동물 수",
                    color='status',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    # 시간에 따른 유기동물 추이
    if 'notice_date' in filtered_df.columns:
        st.subheader("시간에 따른 유기동물 발생 추이")
        
        # 월별 집계
        filtered_df['year_month'] = filtered_df['notice_date'].dt.strftime('%Y-%m')
        monthly_counts = filtered_df.groupby('year_month').size().reset_index(name='count')
        
        fig = px.line(monthly_counts, x='year_month', y='count', 
                     title="월별 유기동물 발생 추이",
                     markers=True)
        fig.update_layout(xaxis_title="년월", yaxis_title="유기동물 수")
        st.plotly_chart(fig, use_container_width=True)