import streamlit as st
import pandas as pd

st.title("🚇 지하철 이용자 수 조회")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    try:
        # 열 이름은 우리가 직접 지정하고, 사용할 열만 골라 읽음 (1: 노선명, 2: 역명, 3: 승차, 4: 하차)
        df = pd.read_csv(
            uploaded_file,
            header=0,  # 헤더가 있는 경우: 0 / 없는 경우: None
            usecols=[1, 2, 3, 4],
            names=["노선명", "역명", "승차총승객수", "하차총승객수"],
            skiprows=1  # 첫 줄이 헤더인 경우 생략
        )

        # 노선 선택
        selected_line = st.selectbox("노선명을 선택하세요", sorted(df["노선명"].unique()))

        # 역 선택
        stations = sorted(df[df["노선명"] == selected_line]["역명"].unique())
        selected_station = st.selectbox(f"{selected_line}의 역명을 선택하세요", stations)

        # 필터링
        filtered = df[(df["노선명"] == selected_line) & (df["역명"] == selected_station)]

        # 합계 계산
        total_boarding = filtered["승차총승객수"].sum()
        total_alighting = filtered["하차총승객수"].sum()

        # 결과 출력
        st.subheader(f"📊 {selected_line} {selected_station}역 총 이용자 수")
        col1, col2 = st.columns(2)
        col1.metric("총 승차 승객 수", f"{total_boarding:,}명")
        col2.metric("총 하차 승객 수", f"{total_alighting:,}명")

    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
else:
    st.info("CSV 파일을 업로드해주세요. (b열: 노선명, c열: 역명, d열: 승차, e열: 하차)")
