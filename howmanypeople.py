import streamlit as st
import pandas as pd

# 1. CSV 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("subway_data.csv", encoding="utf-8")  # 파일명 및 인코딩 확인
    return df

df = load_data()

# 2. 노선명 선택
lines = sorted(df["노선명"].unique())
selected_line = st.selectbox("노선명을 선택하세요", lines)

# 3. 선택된 노선에 해당하는 역명 목록 필터링
stations = sorted(df[df["노선명"] == selected_line]["역명"].unique())
selected_station = st.selectbox(f"{selected_line}의 역명을 선택하세요", stations)

# 4. 선택된 노선 & 역에 해당하는 데이터 필터링
filtered = df[(df["노선명"] == selected_line) & (df["역명"] == selected_station)]

# 5. 승하차 합계 계산
total_boarding = filtered["승차승객수"].sum()
total_alighting = filtered["하차승객수"].sum()

# 6. 결과 출력
st.subheader(f"🚉 {selected_line} - {selected_station} 역의 총 이용자 수")
st.metric("총 승차 승객 수", f"{total_boarding:,}명")
st.metric("총 하차 승객 수", f"{total_alighting:,}명")
