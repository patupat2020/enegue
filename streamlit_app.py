import streamlit as st
import pandas as pd
import string
from datetime import datetime

# Helper: Generate list of section letters (A, B, C...)
def get_sections(count):
    return list(string.ascii_uppercase[:count])

st.set_page_config(page_title="BNHS DRRM Headcount", page_icon="🚨")
st.title("🚨 BNHS Emergency Headcount")

# --- Input Form ---
with st.form("headcount_form"):
    teacher_name = st.text_input("Adviser Name")
    
    # 1. Choose Division (Determines the next options)
    division = st.radio("Select Division", ["JHS", "SHS"], horizontal=True)
    
    # Initialize variables
    section_label = ""
    grade = None
    
    # 2. Logic for Grade Levels based on Division
    if division == "JHS":
        grade = st.selectbox("Grade Level", [7, 8, 9, 10])
        
        # Section logic for JHS
        if grade == 7:
            section = st.selectbox("Section", get_sections(15)) # A-O
        else:
            section = st.selectbox("Section", get_sections(14)) # A-N
        
        section_label = f"JHS - Grade {grade} - {section}"
        
    else: # SHS Division
        grade = st.selectbox("Grade Level", [11, 12])
        track = st.radio("Track", ["TechPro", "Academics"], horizontal=True)
        
        # Section logic for SHS
        if track == "TechPro":
            section = st.selectbox("Section", get_sections(10)) # A-J
        else:
            section = st.selectbox("Section", get_sections(12)) # A-L
            
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
        st.success(f"Report submitted for {section_label}. Stay safe!")

# --- Coordinator Dashboard ---
if st.sidebar.checkbox("Coordinator: View Master List"):
    if pd.io.common.file_exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.write("### Current Headcount Status")
        st.dataframe(df)
        
        # Quick metrics
        st.metric("Total Missing Students", df['Missing'].sum())
        
        if st.button("Reset/Clear Data"):
            import os
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
                st.rerun()
    else:
        st.write("No data recorded.")
