import streamlit as st
import pandas as pd
import string
from datetime import datetime

# Helper: Generate list of section letters
def get_sections(count):
    return list(string.ascii_uppercase[:count])

st.set_page_config(page_title="BNHS DRRM Headcount", page_icon="🚨")
st.title("🚨 BNHS Emergency Headcount")

# --- Input Form ---
with st.form("headcount_form"):
    teacher_name = st.text_input("Adviser Name")
    
    # 1. Level Selection (The top-level gatekeeper)
    division = st.radio("Select Division", ["JHS", "SHS"], horizontal=True)
    
    section_label = ""
    
    if division == "JHS":
        grade = st.selectbox("Grade Level", [7, 8, 9, 10])
        if grade == 7:
            # A-O
            section = st.selectbox("Section", get_sections(15))
        else:
            # A-N
            section = st.selectbox("Section", get_sections(14))
        section_label = f"JHS - Grade {grade} - {section}"
        
    else: # SHS Division
        grade = st.selectbox("Grade Level", [11, 12])
        track = st.radio("Track", ["TechPro", "Academics"], horizontal=True)
        
        if track == "TechPro":
            # A-J
            section = st.selectbox("Section", get_sections(10))
        else:
            # A-L
            section = st.selectbox("Section", get_sections(12))
        section_label = f"SHS - Grade {grade} - {track} - {section}"

    col1, col2 = st.columns(2)
    with col1:
        present = st.number_input("Students Present", min_value=0, step=1)
    with col2:
        missing = st.number_input("Students Missing", min_value=0, step=1)
    
    submit = st.form_submit_button("Submit Headcount")

# --- Submission Logic ---
DATA_FILE = "headcount_log.csv"

if submit:
    if not teacher_name:
        st.error("Please enter your name.")
    else:
        entry = {
            'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'Teacher': [teacher_name],
            'Level': [division],
            'Section_Info': [section_label],
            'Present': [present],
            'Missing': [missing]
        }
        
        df = pd.DataFrame(entry)
        header = False if pd.io.common.file_exists(DATA_FILE) else True
        df.to_csv(DATA_FILE, mode='a', header=header, index=False)
        st.success(f"Report submitted for {section_label}.")

# --- Coordinator Dashboard ---
if st.sidebar.checkbox("Coordinator: View Master List"):
    if pd.io.common.file_exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.write("### Current Headcount Status")
        st.dataframe(df)
        
        # Quick summary metrics
        st.metric("Total Missing Students", df['Missing'].sum())
        
        if st.button("Reset/Clear Data"):
            import os
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
                st.rerun()
    else:
        st.write("No data recorded.")
