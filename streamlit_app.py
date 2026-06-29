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

# --- 1. SELECTION LOGIC (Outside the form for instant updates) ---
teacher_name = st.text_input("Adviser Name")

division = st.radio("Select Division", ["JHS", "SHS"], index=None, horizontal=True)

grade = None
section = None
section_label = ""

if division == "JHS":
    grade = st.selectbox("Grade Level", [7, 8, 9, 10], index=None)
    if grade:
        count = 15 if grade == 7 else 14
        section = st.selectbox("Section", get_sections(count), index=None)
        if section: section_label = f"JHS - Grade {grade} - {section}"

elif division == "SHS":
    grade = st.selectbox("Grade Level", [11, 12], index=None)
    if grade:
        track = st.radio("Track", ["TechPro", "Academics"], index=None, horizontal=True)
        if track:
            count = 10 if track == "TechPro" else 12
            section = st.selectbox("Section", get_sections(count), index=None)
            if section: section_label = f"SHS - Grade {grade} - {track} - {section}"

# --- 2. INPUT FORM (Only for final entry and submission) ---
# Only show the form if they have finished making selections
if section_label:
    st.write("---")
    with st.form("headcount_form"):
        col1, col2 = st.columns(2)
        with col1:
            present = st.number_input("Students Present", min_value=0, step=1)
        with col2:
            missing = st.number_input("Students Missing", min_value=0, step=1)
        
        submit = st.form_submit_button("Submit Headcount")

    # --- 3. SUBMISSION LOGIC ---
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
