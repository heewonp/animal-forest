import streamlit as st
import plotly.express as px

def show_animal_traits(filtered_df):
    """동물 특성 분석 페이지를 표시합니다."""
    st.title("동물 특성 분석")
    
    # 품종 분석
    st.header("품종 분석")
    if 'breed' in filtered_df.columns and 'animal_type' in filtered_df.columns:
        # 동물 유형 선택
        animal_types = ['전체'] + sorted(filtered_df['animal_type'].unique().tolist())
        selected_type = st.selectbox("동물 종류 선택", animal_types)
        
        # 선택된 동물 유형으로 필터링
        if selected_type == '전체':
            type_filtered_df = filtered_df
        else:
            type_filtered_df = filtered_df[filtered_df['animal_type'] == selected_type]
        
        # 상위 10개 품종 표시
        breed_counts = type_filtered_df['breed'].value_counts().head(10).reset_index()
        breed_counts.columns = ['breed', 'count']
        
        fig = px.bar(breed_counts, x='breed', y='count', 
                    title=f"상위 10개 {selected_type} 품종",
                    color='breed',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    # 색상 분석
    st.header("색상 분석")
    if 'color_type' in filtered_df.columns and 'color_cat' in filtered_df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # 색상 타입 분포
            color_type_counts = filtered_df['color_type'].value_counts().reset_index()
            color_type_counts.columns = ['color_type', 'count']
            
            fig = px.pie(color_type_counts, values='count', names='color_type', 
                        title="색상 타입 분포",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 색상 카테고리 상위 분포
            color_cat_counts = filtered_df['color_cat'].value_counts().head(8).reset_index()
            color_cat_counts.columns = ['color_cat', 'count']
            
            fig = px.bar(color_cat_counts, x='color_cat', y='count', 
                        title="상위 색상 카테고리",
                        color='color_cat',
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
    
    # 성별 및 중성화 분석
    st.header("성별 및 중성화 분석")
    if 'animal_status' in filtered_df.columns:
        status_counts = filtered_df['animal_status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        
        fig = px.pie(status_counts, values='count', names='status', 
                    title="성별 및 중성화 상태",
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    # 체중 분석
    st.header("체중 분석")
    if 'weight' in filtered_df.columns and 'animal_type' in filtered_df.columns:
        # 체중 데이터가 있는 행만 필터링
        weight_df = filtered_df[filtered_df['weight'].notna()]
        
        if not weight_df.empty:
            animal_types = sorted(weight_df['animal_type'].unique().tolist())
            selected_type = st.selectbox("체중 분석할 동물 종류 선택", animal_types, key="weight_select")
            
            type_weight_df = weight_df[weight_df['animal_type'] == selected_type]
            
            if not type_weight_df.empty:
                fig = px.histogram(type_weight_df, x='weight', 
                                  title=f"{selected_type} 체중 분포",
                                  color_discrete_sequence=px.colors.qualitative.Pastel,
                                  nbins=20)
                st.plotly_chart(fig, use_container_width=True)
                
                # 체중 통계량
                stats = type_weight_df['weight'].describe()
                st.metric(f"{selected_type} 평균 체중", f"{stats['mean']:.2f}kg")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("최소 체중", f"{stats['min']:.2f}kg")
                with col2:
                    st.metric("중앙값", f"{stats['50%']:.2f}kg")
                with col3:
                    st.metric("최대 체중", f"{stats['max']:.2f}kg")
            else:
                st.warning(f"{selected_type}의 체중 데이터가 없습니다.")
        else:
            st.warning("체중 데이터가 없습니다.")