import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# 인증 및 시트 접근 설정
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# secrets.toml에서 서비스 계정 정보 불러오기
credentials = Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=SCOPES
)

# gspread로 인증
gc = gspread.authorize(credentials)

# 스프레드시트 열기
spreadsheet = gc.open_by_key(st.secrets["gsheet_key"])
sheet_input = spreadsheet.worksheet("datainput")
sheet_view = spreadsheet.worksheet("dataview")

# dataview 시트 데이터 불러오기
def load_view_data():
    data = sheet_view.get_all_records()
    return pd.DataFrame(data)

# datainput 시트에 입력 데이터 추가
def append_input_data(name, feedback):
    sheet_input.append_row([name, feedback])

# Streamlit 인터페이스
st.title("📄 양방향 Google Sheets 데이터 웹앱")

# 입력 폼
with st.form("input_form"):
    name = st.text_input("Name")
    feedback = st.text_area("Feedback")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if name and feedback:
            append_input_data(name, feedback)
            st.success("✅ Your response has been saved.")
        else:
            st.warning("Please fill in all fields.")

st.markdown("---")

# 데이터 출력
st.subheader("📊 Data from 'dataview' Sheet")
df = load_view_data()
st.dataframe(df)
