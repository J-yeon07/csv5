import streamlit as st
import pandas as pd
import io

def app():
    st.set_page_config(layout="wide")
    st.title("CSV 파일 특정 부분 추출기")

    st.write(
        """
        이 앱은 CSV 파일을 업로드하여 특정 열(Column)을 선택하거나, 특정 조건으로 행(Row)을 필터링하여 데이터를 추출할 수 있도록 도와줍니다.
        """
    )

    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

    if uploaded_file is not None:
        try:
            # 파일을 바이트 스트림으로 읽고 pandas DataFrame으로 변환
            dataframe = pd.read_csv(uploaded_file)
            st.success("파일이 성공적으로 업로드되었습니다.")
            st.subheader("원본 데이터 미리보기")
            st.dataframe(dataframe.head())

            st.markdown("---")
            st.subheader("1. 열(Column) 선택")

            all_columns = dataframe.columns.tolist()
            selected_columns = st.multiselect(
                "추출할 열을 선택하세요:",
                options=all_columns,
                default=all_columns # 기본적으로 모든 열 선택
            )

            if selected_columns:
                df_selected_columns = dataframe[selected_columns]
                st.subheader("선택된 열 데이터")
                st.dataframe(df_selected_columns)

                # 선택된 열 데이터 다운로드 버튼
                csv_buffer_columns = io.StringIO()
                df_selected_columns.to_csv(csv_buffer_columns, index=False, encoding='utf-8-sig')
                st.download_button(
                    label="선택된 열 CSV 다운로드",
                    data=csv_buffer_columns.getvalue(),
                    file_name="selected_columns.csv",
                    mime="text/csv",
                )
            else:
                st.warning("적어도 하나 이상의 열을 선택해주세요.")

            st.markdown("---")
            st.subheader("2. 행(Row) 필터링")

            filter_option = st.radio(
                "필터링 방식을 선택하세요:",
                ("필터링 없음", "특정 열 값으로 필터링", "특정 문자열 포함 여부로 필터링")
            )

            df_filtered = dataframe.copy() # 필터링을 위한 복사본

            if filter_option == "특정 열 값으로 필터링":
                filter_column = st.selectbox("필터링할 열을 선택하세요:", options=all_columns)
                if filter_column:
                    column_dtype = dataframe[filter_column].dtype
                    if pd.api.types.is_numeric_dtype(column_dtype):
                        st.write(f"선택된 열 '{filter_column}'은 숫자형입니다.")
                        filter_type = st.radio(
                            "필터링 조건 선택:",
                            ("보다 크거나 같음 (>=)", "보다 작거나 같음 (<=)", "같음 (==)", "범위 (min ~ max)")
                        )
                        if filter_type == "보다 크거나 같음 (>=)":
                            filter_value = st.number_input(f"'{filter_column}'의 최소값을 입력하세요:", value=0.0)
                            df_filtered = df_filtered[df_filtered[filter_column] >= filter_value]
                        elif filter_type == "보다 작거나 같음 (<=)":
                            filter_value = st.number_input(f"'{filter_column}'의 최대값을 입력하세요:", value=0.0)
                            df_filtered = df_filtered[df_filtered[filter_column] <= filter_value]
                        elif filter_type == "같음 (==)":
                            unique_values = dataframe[filter_column].unique().tolist()
                            if len(unique_values) > 100: #
