import streamlit as st
import pandas as pd
import plotly.express as px
from database import init_db, register_user, login_user, add_health_log, get_user_logs
from ai_utils import get_sentiment, get_ai_advice, get_risk_prediction

init_db()
st.set_page_config(page_title="孕婦健康紀錄系統", layout="wide")

if 'user' not in st.session_state: st.session_state.user = None

def main():
    if st.session_state.user is None:
        st.title("🤰 登入 / 註冊")
        tab1, tab2 = st.tabs(["登入", "註冊"])
        with tab1:
            email = st.text_input("電子郵件")
            pwd = st.text_input("密碼", type="password")
            if st.button("登入"):
                user = login_user(email, pwd)
                if user: 
                    st.session_state.user = user
                    st.rerun()
        with tab2:
            new_email = st.text_input("註冊電子郵件")
            new_pwd = st.text_input("註冊密碼", type="password")
            nickname = st.text_input("暱稱")
            if st.button("註冊"):
                if register_user(new_email, new_pwd, nickname): st.success("註冊成功")
    else:
        st.sidebar.title(f"你好, {st.session_state.user['nickname']}")
        page = st.sidebar.radio("導覽", ["健康日誌", "數據儀錶板", "營養建議", "AI 風險預警"])
        
        if page == "健康日誌":
            st.header("📝 健康日誌")
            # 顯示手環同步狀態與最新數據邏輯... (略，見前次完整範例)
            with st.form("log_form"):
                week = st.number_input("週數", 1, 42, 20)
                weight = st.number_input("體重", 30.0, 150.0, 60.0)
                notes = st.text_area("其他補充 (情感分析)")
                if st.form_submit_button("儲存"):
                    sentiment = get_sentiment(notes)
                    add_health_log(st.session_state.user['id'], {"week": week, "weight": weight, "notes": notes, "sentiment": sentiment})
                    st.success(f"已儲存！情感分析：{sentiment}")
        
        elif page == "數據儀錶板":
            logs = get_user_logs(st.session_state.user['id'])
            if logs:
                df = pd.DataFrame([dict(log) for log in logs])
                st.plotly_chart(px.line(df, x='created_at', y='weight', title="體重趨勢"))
        
        if st.sidebar.button("登出"):
            st.session_state.user = None
            st.rerun()

if __name__ == "__main__":
    main()
