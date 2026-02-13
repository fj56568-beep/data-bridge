import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Excel Bridge", layout="wide")

st.title("Excel-to-Extension Direct Bridge")

# --- RESET LOGIC ---
if st.sidebar.button("Hard Reset / Clear Cache"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# Initialize data list
rows_to_process = []

# --- OPTION 1: CSV UPLOAD ---
st.subheader("Method A: Upload CSV")
uploaded_file = st.file_uploader("Upload CSV file", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    # Force first two columns only
    rows_to_process = df.iloc[:, :2].values.tolist()

# --- OPTION 2: MANUAL PASTE ---
st.subheader("Method B: Paste from Excel")
# Added a unique key to force the widget to update
pasted_text = st.text_area("Paste your Excel rows here", height=150, key="excel_input")

if pasted_text:
    lines = pasted_text.strip().split('\n')
    pasted_data = []
    for line in lines:
        parts = line.split('\t')
        just = parts[0] if len(parts) > 0 else ""
        desc = parts[1] if len(parts) > 1 else ""
        # Filter out the headers and old technical jargon
        if "Justification" not in just and just != "":
            pasted_data.append([just, desc])
    rows_to_process = pasted_data

# --- FINAL DISPLAY ---
if rows_to_process:
    st.divider()
    st.subheader("Current Preview (Check if this matches your Excel!)")
    
    # Create the DataFrame
    preview_df = pd.DataFrame(rows_to_process, columns=["Justification", "Content Description"])
    
    # Show the table
    st.dataframe(preview_df, use_container_width=True, height=400)

    # Generate the code
    extension_code = json.dumps(rows_to_process)
    st.subheader("Copy this code for your Extension:")
    st.code(extension_code, language="json")
