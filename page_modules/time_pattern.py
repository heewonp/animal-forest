import streamlit as st
import plotly.express as px
import pandas as pd

def show_time_pattern(filtered_df):
    """시간 패턴 분석 페이지를 표시합니다."""
    st.title("시간 패턴 분석")
    
    # 연도별 추이
    st.header("연도별 유기동물 발생 추이")
    year_column = None
   
    # 전처리된 연도 컬럼 찾기
    if 'happen_year' in filtered_df.columns:
        year_column = 'happen_year'
    
    if year_column:
        # 전처리된 연도 컬럼 사용
        yearly_counts = filtered_df.groupby(year_column).size().reset_index(name='count')
        
        fig = px.line(yearly_counts, x=year_column, y='count', 
                     title="연도별 유기동물 발생 추이",
                     markers=True)
        fig.update_layout(xaxis_title="연도", yaxis_title="유기동물 수")
        st.plotly_chart(fig, use_container_width=True)
    
    # 월별 패턴
    st.header("월별 유기동물 발생 패턴")
    month_column = None
    month_name_column = None
    
    # 전처리된 월 컬럼 찾기
    if 'happen_month' in filtered_df.columns:
        month_column = 'happen_month'
    
    # 전처리된 월 이름 컬럼 찾기
    if 'month_name' in filtered_df.columns:
        month_name_column = 'month_name'
    
    if month_column:
        if month_name_column and month_name_column in filtered_df.columns:
            # 전처리된 월 이름 컬럼 사용
            monthly_counts = filtered_df.groupby([month_column, month_name_column]).size().reset_index(name='count')
            x_col = month_name_column
        else:
            # 월 이름 추가
            monthly_counts = filtered_df.groupby(month_column).size().reset_index(name='count')
            month_names = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
            monthly_counts['month_name'] = monthly_counts[month_column].apply(lambda x: month_names[x-1])
            x_col = 'month_name'
        
        fig = px.bar(monthly_counts, x=x_col, y='count', 
                    title="월별 유기동물 발생 패턴",
                    color=x_col,
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(xaxis_title="월", yaxis_title="유기동물 수")
        st.plotly_chart(fig, use_container_width=True)
    
    # 요일별 패턴
    st.header("요일별 유기동물 발생 패턴")
    weekday_column = None
    weekday_name_column = None
    
    # 전처리된 요일 컬럼 찾기
    if 'happen_weekday' in filtered_df.columns:
        weekday_column = 'happen_weekday'
    
    # 전처리된 요일 이름 컬럼 찾기
    if 'happen_dayofweek' in filtered_df.columns:
        weekday_name_column = 'happen_dayofweek'
    
    if weekday_column:
        if weekday_name_column and weekday_name_column in filtered_df.columns:
            # 전처리된 요일 이름 컬럼 사용
            weekday_counts = filtered_df.groupby([weekday_column, weekday_name_column]).size().reset_index(name='count')
            x_col = weekday_name_column
        else:
            # 요일 이름 추가
            weekday_counts = filtered_df.groupby(weekday_column).size().reset_index(name='count')
            weekday_names = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
            weekday_counts['weekday_name'] = weekday_counts[weekday_column].apply(lambda x: weekday_names[x])
            x_col = 'weekday_name'
        
        fig = px.bar(weekday_counts, x=x_col, y='count', 
                    title="요일별 유기동물 발생 패턴",
                    color=x_col,
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(xaxis_title="요일", yaxis_title="유기동물 수")
        st.plotly_chart(fig, use_container_width=True)
    
    # 계절별 패턴
    st.header("계절별 유기동물 발생 패턴")
    season_column = None
    
    # 전처리된 계절 컬럼 찾기
    if 'happen_season' in filtered_df.columns:
        season_column = 'happen_season'

    if season_column:
        # 전처리된 계절 컬럼 사용
        season_counts = filtered_df.groupby(season_column).size().reset_index(name='count')
        
        # 계절 순서 정렬
        season_order = ['봄', '여름', '가을', '겨울']
        season_counts['season_order'] = season_counts[season_column].apply(lambda x: season_order.index(x))
        season_counts = season_counts.sort_values('season_order')
        
        fig = px.pie(season_counts, values='count', names=season_column, 
                    title="계절별 유기동물 발생 비율",
                    color=season_column,
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    # 월별 동물 유형 분포
    st.header("월별 동물 유형 분포")
    if month_column and 'animal_type' in filtered_df.columns:
        # 월별, 동물 유형별 집계
        month_animal_counts = pd.crosstab(filtered_df[month_column], filtered_df['animal_type']).reset_index()
        
        # Melt 데이터프레임으로 변환
        melted_df = pd.melt(month_animal_counts, id_vars=[month_column], var_name='animal_type', value_name='count')
        
        # 월 이름 추가
        if not 'month_name' in melted_df.columns:
            month_names = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
            melted_df['month_name'] = melted_df[month_column].apply(lambda x: month_names[x-1])
        
        fig = px.bar(melted_df, x='month_name', y='count', color='animal_type',
                     title="월별 동물 유형 분포",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(xaxis_title="월", yaxis_title="유기동물 수")
        st.plotly_chart(fig, use_container_width=True)