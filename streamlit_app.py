# --- Input Form ---
with st.form("headcount_form"):
    teacher_name = st.text_input("Adviser Name")
    
    division = st.radio("Select Junior High or Senior High", ["JHS", "SHS"], index=None, horizontal=True)
    
    grade = None
    section = None
    section_label = ""
    
    # Selection Logic
    if division == "JHS":
        grade = st.selectbox("Grade Level", [7, 8, 9, 10], index=None)
        if grade:
            if grade == 7:
                section = st.selectbox("Section", get_sections(15), index=None)
            else:
                section = st.selectbox("Section", get_sections(14), index=None)
            if section: section_label = f"JHS - Grade {grade} - {section}"
                
    elif division == "SHS":
        grade = st.selectbox("Grade Level", [11, 12], index=None)
        if grade:
            track = st.radio("Track", ["TechPro", "Academics"], index=None, horizontal=True)
            if track:
                if track == "TechPro":
                    section = st.selectbox("Section", get_sections(10), index=None)
                else:
                    section = st.selectbox("Section", get_sections(12), index=None)
                if section: section_label = f"SHS - Grade {grade} - {track} - {section}"

    # Always show inputs, but they will be empty until choices are made
    col1, col2 = st.columns(2)
    with col1:
        present = st.number_input("Students Present", min_value=0, step=1)
    with col2:
        missing = st.number_input("Students Missing", min_value=0, step=1)
    
    # THE FIX: Always define the button inside the form
    submit = st.form_submit_button("Submit Headcount")

# --- Submission Logic (Moved outside the 'with' block) ---
if submit:
    # Check if they actually filled everything out
    if not teacher_name or not section_label:
        st.error("Please ensure you have selected your Grade, Track/Section, and entered your Name.")
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
