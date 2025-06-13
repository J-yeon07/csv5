import streamlit as st
import pandas as pd

st.title("🚇 지하철 이용자 수 조회")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    try:
        # 1차 시도: UTF-8
        try:
            df = pd.read_csv(
                uploaded_file,
                header=0,
                usecols=[1, 2, 3, 4],
                names=["노선명", "역명", "승차총승객수", "하차총승객수"],
                skiprows=1,
                encoding='utf-8'
            )
        except UnicodeDecodeError:
            # 2차 시도: CP949 (Excel 기본 인코딩)
            uploaded_file.seek(0)  # 파일 포인터 초기화
            df = pd.read_csv(
                uploaded_file,
                header=0,
                usecols=[1, 2, 3, 4],
                names=["노선명", "역명", "승차총승객수", "하차총승객수"],
                skiprows=1,
                encoding='cp949'
            )

        selected_line = st.selectbox("노선명을 선택하세요", sorted(df["노선명"].unique()))
        station_options = sorted(df[df["노선명"] == selected_line]["역명"].unique())
        selected_station = st.selectbox(f"{selected_line}의 역명을 선택하세요", station_options)

        filtered_df = df[(df["노선명"] == selected_line) & (df["역명"] == selected_station)]

        total_boarding = filtered_df["승차총승객수"].sum()
        total_alighting = filtered_df["하차총승객수"].sum()

        st.subheader(f"📊 {selected_line} {selected_station}역 총 이용자 수")
        col1, col2 = st.columns(2)
        col1.metric("총 승차 승객 수", f"{total_boarding:,}명")
        col2.metric("총 하차 승객 수", f"{total_alighting:,}명")

    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
else:
    st.info("CSV 파일을 업로드해주세요. (b열: 노선명, c열: 역명, d열: 승차, e열: 하차)")
