import streamlit as st
import pandas as pd
import string
from datetime import datetime

# Setup
st.set_page_config(page_title="BNHS DRRM Headcount", page_icon="🚨")
st.title("🚨 School Emergency Headcount")

# Helper: Generate list of section letters
# A=0, B=1, ... O=14 (index 15)
def get_sections(count):
    return list(string.ascii_uppercase[:count])

# --- Input Form ---
with st.form("headcount_form"):
    teacher_name = st.text_input("Teacher/Adviser Name")
    grade = st.selectbox("Grade Level", [7, 8, 9, 10, 11, 12])
    
    # Section Logic
    section = None
    section_label = ""
    
    if grade in [7, 8, 9, 10]:
        # JHS Logic
        if grade == 7:
            # A-O (15 letters)
            section = st.selectbox("Section", get_sections(15))
        else:
            # A-N (14 letters)
            section = st.selectbox("Section", get_sections(14))
        section_label = f"Grade {grade} - {section}"
        
    else:
        # SHS Logic (11, 12)
        track = st.radio("SHS Track", ["TechPro", "Academics"])
        if track == "TechPro":
            # A-J (10 letters)
            section = st.selectbox("Section", get_sections(10))
        else:
            # A-L (12 letters)
            section = st.selectbox("Section", get_sections(12))
        section_label = f"Grade {grade} - {track} - {section}"

    present = st.number_input("Students Present", min_value=0, step=1)
    missing = st.number_input("Students Missing/Unaccounted", min_value=0, step=1)
    
    submit = st.form_submit_button("Submit Headcount")

# --- Submission Logic ---
DATA_FILE = "headcount_log.csv"

if submit:
    if not teacher_name:
        st.error("Please enter your name.")
    else:
        # Create a dictionary for the new entry
        entry = {
            'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'Teacher': [teacher_name],
            'Section_Info': [section_label],
            'Present': [present],
            'Missing': [missing]
        }
        
        # Save to CSV
        df = pd.DataFrame(entry)
        # Write to file (create if not exists)
        header = False if pd.io.common.file_exists(DATA_FILE) else True
        df.to_csv(DATA_FILE, mode='a', header=header, index=False)
        
        st.success(f"Report submitted for {section_label}. Stay safe!")

# --- Coordinator View ---
if st.sidebar.checkbox("Coordinator: View Master List"):
    if pd.io.common.file_exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.write("### Current Headcount Status")
        st.dataframe(df)
        
        # Simple summary
        total_missing = df['Missing'].sum()
        st.metric("Total Missing Students", total_missing)
        
        if st.button("Clear Records"):
            # Caution: In real usage, maybe archive instead of deleting
            import os
            os.remove(DATA_FILE)
            st.rerun()
    else:
        st.write("No data recorded yet.")
