import streamlit as st
import pandas as pd

st.title("🚇 지하철 이용자 수 조회")

# 1. 사용자로부터 CSV 파일 업로드 받기
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    try:
        # 2. 업로드된 CSV 파일 읽기
        df = pd.read_csv(uploaded_file)

        # 3. 필요한 열이 존재하는지 확인
        required_columns = {'노선명', '역명', '승차승객수', '하차승객수'}
        if not required_columns.issubset(df.columns):
            st.error("❗ CSV 파일에 필요한 열이 없습니다. '노선명', '역명', '승차승객수', '하차승객수' 열이 모두 있어야 합니다.")
        else:
            # 4. 노선명 선택
            line_options = sorted(df["노선명"].unique())
            selected_line = st.selectbox("노선명을 선택하세요", line_options)

            # 5. 선택된 노선의 역명만 필터링
            station_options = sorted(df[df["노선명"] == selected_line]["역명"].unique())
            selected_station = st.selectbox(f"{selected_line}의 역명을 선택하세요", station_options)

            # 6. 선택된 노선명과 역명으로 필터링
            filtered_df = df[(df["노선명"] == selected_line) & (df["역명"] == selected_station)]

            # 7. 승하차 인원 합계 계산
            total_boarding = filtered_df["승차승객수"].sum()
            total_alighting = filtered_df["하차승객수"].sum()

            # 8. 결과 출력
            st.subheader(f"📊 {selected_line} {selected_station}역 총 이용자 수")
            col1, col2 = st.columns(2)
            col1.metric("총 승차 승객 수", f"{total_boarding:,}명")
            col2.metric("총 하차 승객 수", f"{total_alighting:,}명")

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.info("왼쪽에서 CSV 파일을 먼저 업로드하세요.")
