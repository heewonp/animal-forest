import streamlit as st
import plotly.express as px
import pandas as pd

def show_survival_factors(filtered_df):
    """생존 요인 분석 페이지를 표시합니다."""
    st.title("생존 요인 분석")
    
    # 필요한 열이 있는지 확인
    if 'process_state' in filtered_df.columns:
        # 상태 분류
        outcome_categories = {
            '보호중': '보호중',
            '입양': '입양됨',
            '반환': '반환됨',
            '자연사': '사망',
            '안락사': '사망',
            '방사': '기타',
            '기증': '기타',
            '기타': '기타'
        }
        
        # 상태 매핑
        filtered_df['outcome'] = filtered_df['process_state'].map(
            lambda x: outcome_categories.get(x, '기타')
        )
        
        # 결과별 카운트
        outcome_counts = filtered_df['outcome'].value_counts().reset_index()
        outcome_counts.columns = ['outcome', 'count']
        
        # 전체 결과 파이 차트
        st.header("유기동물 최종 상태 분포")
        fig = px.pie(outcome_counts, values='count', names='outcome', 
                    title="유기동물 최종 상태 분포",
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
        
        # 성별에 따른 결과
        st.header("성별에 따른 결과")
        if 'sex_cd' in filtered_df.columns:
            sex_outcome = pd.crosstab(filtered_df['sex_cd'], filtered_df['outcome']).reset_index()
            sex_outcome_melted = pd.melt(sex_outcome, id_vars=['sex_cd'], 
                                        value_vars=outcome_counts['outcome'].tolist(),
                                        var_name='outcome', value_name='count')
            
            fig = px.bar(sex_outcome_melted, x='sex_cd', y='count', color='outcome',
                        title="성별에 따른 결과 분포",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        
        # 중성화 여부에 따른 결과
        st.header("중성화 여부에 따른 결과")
        if 'neuter_yn' in filtered_df.columns:
            neuter_outcome = pd.crosstab(filtered_df['neuter_yn'], filtered_df['outcome']).reset_index()
            neuter_outcome_melted = pd.melt(neuter_outcome, id_vars=['neuter_yn'], 
                                           value_vars=outcome_counts['outcome'].tolist(),
                                           var_name='outcome', value_name='count')
            
            fig = px.bar(neuter_outcome_melted, x='neuter_yn', y='count', color='outcome',
                        title="중성화 여부에 따른 결과 분포",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        
        # 동물 종류에 따른 결과
        st.header("동물 종류에 따른 결과")
        if 'animal_type' in filtered_df.columns:
            type_outcome = pd.crosstab(filtered_df['animal_type'], filtered_df['outcome']).reset_index()
            type_outcome_melted = pd.melt(type_outcome, id_vars=['animal_type'], 
                                         value_vars=outcome_counts['outcome'].tolist(),
                                         var_name='outcome', value_name='count')
            
            fig = px.bar(type_outcome_melted, x='animal_type', y='count', color='outcome',
                        title="동물 종류에 따른 결과 분포",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        
        # 체중에 따른 결과 (개만)
        st.header("체중에 따른 결과 (개)")
        if 'weight' in filtered_df.columns and 'animal_type' in filtered_df.columns:
            # 개만 필터링
            dogs_df = filtered_df[(filtered_df['animal_type'] == '개') & (filtered_df['weight'].notna())]
            
            if not dogs_df.empty:
                # 체중 구간 생성
                dogs_df['weight_range'] = pd.cut(
                    dogs_df['weight'], 
                    bins=[0, 5, 10, 15, 20, 25, 30, 100],
                    labels=['0-5kg', '5-10kg', '10-15kg', '15-20kg', '20-25kg', '25-30kg', '30kg+']
                )
                
                # 체중 구간별 결과 분포
                weight_outcome = pd.crosstab(dogs_df['weight_range'], dogs_df['outcome']).reset_index()
                weight_outcome_melted = pd.melt(weight_outcome, id_vars=['weight_range'], 
                                              value_vars=outcome_counts['outcome'].tolist(),
                                              var_name='outcome', value_name='count')
                
                fig = px.bar(weight_outcome_melted, x='weight_range', y='count', color='outcome',
                            title="체중에 따른 결과 분포 (개)",
                            color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("개의 체중 데이터가 없습니다.")
    else:
        st.warning("동물 상태 정보가 데이터에 없습니다.")