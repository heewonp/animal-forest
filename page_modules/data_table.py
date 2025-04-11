import streamlit as st
import pandas as pd
import io

def show_data_table(filtered_df):
    """데이터 테이블 페이지를 표시합니다."""
    st.title("데이터 테이블")
    
    # 컬럼 선택 옵션
    all_columns = filtered_df.columns.tolist()
    selected_columns = st.multiselect("표시할 컬럼 선택", all_columns, default=all_columns[:10])
    
    # 검색 필터
    search_term = st.text_input("검색어 입력 (모든 컬럼에서 검색)")
    
    # 검색어로 필터링
    if search_term:
        filtered_data = filtered_df[
            filtered_df.astype(str).apply(
                lambda row: row.str.contains(search_term, case=False).any(), 
                axis=1
            )
        ]
    else:
        filtered_data = filtered_df
    
    # 컬럼 선택하여 표시
    if selected_columns:
        st.dataframe(filtered_data[selected_columns], height=600)
    else:
        st.warning("표시할 컬럼을 하나 이상 선택하세요.")
    
    # 데이터 통계 표시
    st.header("데이터 통계")
    st.write(f"총 행 수: {len(filtered_df)}")
    
    # 숫자형 컬럼 통계
    numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        st.subheader("숫자형 컬럼 통계")
        st.dataframe(filtered_df[numeric_cols].describe())
    
    # 데이터 내보내기 옵션
    st.header("데이터 내보내기")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("CSV로 내보내기"):
            csv = filtered_data[selected_columns].to_csv(index=False)
            st.download_button(
                label="CSV 다운로드",
                data=csv,
                file_name="filtered_animal_data.csv",
                mime="text/csv",
            )
    
    with col2:
        if st.button("Excel로 내보내기"):
            # 메모리에 Excel 파일 생성
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                filtered_data[selected_columns].to_excel(writer, index=False, sheet_name="Data")
            excel_data = output.getvalue()
            
            st.download_button(
                label="Excel 다운로드",
                data=excel_data,
                file_name="filtered_animal_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )