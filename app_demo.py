import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="알바 가디언 (Demo)", layout="wide")

# 2. 제목
st.title("🛡️ Alba Guardian : 급여 정산 시스템 (Demo)")
st.markdown("---")
st.info("📢 이 사이트는 **데모 버전**입니다. 실제 DB 대신 **사전 집계된 데이터(CSV)**를 보여줍니다.")

# 3. 데이터 불러오기
@st.cache_data
def load_data():
    # 같은 폴더에 있는 data.csv를 읽어옵니다.
    return pd.read_csv('data.csv')

try:
    df = load_data()

    # 4. 핵심 지표 (KPI) 보여주기
    total_pay = df['total_salary'].sum()
    st.metric("💰 이번 달 총 지출 인건비", f"{int(total_pay):,}원")

    # 5. 레이아웃 나누기 (왼쪽: 표 / 오른쪽: 그래프)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 직원별 급여 내역")
        # 숫자 포맷 예쁘게 적용
        st.dataframe(
            df.style.format("{:,.0f}원", subset=['basic_pay', 'night_pay', 'holiday_pay', 'juhyu_pay', 'total_salary']),
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.subheader("📊 인건비 비교 그래프")
        # 이름(worker_name)을 기준으로 총 급여(total_salary) 그래프 그리기
        chart_data = df.set_index('worker_name')['total_salary']
        st.bar_chart(chart_data)

except Exception as e:
    st.error(f"❌ 데이터 파일을 읽을 수 없습니다. (에러: {e})")