import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="DRRM Headcount", page_icon="🚨")
st.title("🚨 School Emergency Headcount")

# Initialize a simple CSV file to store data
DATA_FILE = "headcount_data.csv"

def save_data(teacher, section, present, missing):
    data = {'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'Teacher': [teacher],
            'Section': [section],
            'Present': [present],
            'Missing': [missing]}
    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, mode='a', header=False, index=False)

with st.form("headcount_form"):
    teacher = st.text_input("Adviser Name")
    section = st.text_input("Section")
    present = st.number_input("Students Present", min_value=0)
    missing = st.number_input("Students Missing/Unaccounted", min_value=0)
    
    submit = st.form_submit_button("Submit Headcount")
    
    if submit:
        save_data(teacher, section, present, missing)
        st.success(f"Report submitted for {section}. Stay safe!")

# Coordinator view (Hidden behind a password or sidebar)
if st.sidebar.checkbox("View Master List"):
    try:
        df = pd.read_csv(DATA_FILE, names=['Timestamp', 'Teacher', 'Section', 'Present', 'Missing'])
        st.dataframe(df)
    except:
        st.write("No data yet.")