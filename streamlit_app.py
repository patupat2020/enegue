import streamlit as st
import pandas as pd
import string
from datetime import datetime
import os

# Helper: Generate list of section letters
def get_sections(count):
    return list(string.ascii_uppercase[:count])

st.set_page_config(page_title="BNHS DRRM Headcount", page_icon="🚨")
st.title("🚨 BNHS Emergency Headcount")

# --- Input Form ---
with st.form("headcount_form"):
    teacher_name = st.text_input("Adviser Name")
    
    # 1. No default division selected
    division = st.radio("Select Division", ["JHS", "SHS"], index=None, horizontal=True)
    
    grade = None
    section = None
    section_label = ""
    
    # 2. Logic to show fields only after selection
    if division == "JHS":
        grade = st.selectbox("Grade Level", [7, 8, 9, 10], index=None)
        if grade:
            # Section logic for JHS
            if grade == 7:
                section = st.selectbox("Section", get_sections(15), index=None) # A-O
            else:
                section = st.selectbox("Section", get_sections(14), index=None) # A-N
            
            if section:
                section_label = f"JHS - Grade {grade} - {section}"
                
    elif division == "SHS":
        grade = st.selectbox("Grade Level", [11, 12], index=None)
        if grade:
            track = st.radio("Track", ["TechPro", "Academics"], index=None, horizontal=True)
            if track:
                if track == "TechPro":
                    section = st.selectbox("Section", get_sections(10), index=None) # A-J
                else:
                    section = st.selectbox("Section", get_sections(12), index=None) # A-L
                
                if section:
                    section_label = f"SHS - Grade {grade} - {track} - {section}"

    # Only show headcount inputs if all fields are selected
    if section_label:
        col1, col2 = st.columns(2)
        with col1:
            present = st.number_input("Students Present", min_value=0, step=1)
        with col2:
            missing = st.number_input("Students Missing", min_value=0, step=1)
        
        submit = st.form_submit_button("Submit Headcount")
    else:
        submit = None

# --- Submission Logic ---
DATA_FILE = "headcount_log.csv"

if submit:
    if not teacher_name:
        st.error("Please enter your name.")
    elif not section_label or section is None:
        st.error("Please ensure all fields (Grade, Track, Section) are selected.")
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
        header = False if os.path.exists(DATA_FILE) else True
        df.to_csv(DATA_FILE, mode='a', header=header, index=False)
        st.success(f"Report submitted for {section_label}. Stay safe!")

# --- Coordinator Dashboard ---
if st.sidebar.checkbox("Coordinator: View Master List"):
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.write("### Current Headcount Status")
        st.dataframe(df)
        
        st.metric("Total Missing Students", int(df['Missing'].sum()))
        
        if st.button("Reset/Clear Data"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
                st.rerun()
    else:
        st.write("No data recorded.")
