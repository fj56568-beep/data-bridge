import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Data Bridge", layout="wide")

st.title("Excel-to-Extension Direct Bridge")

# Initialize data_rows in session state so it persists during edits
if 'data_rows' not in st.session_state:
    st.session_state.data_rows = []

# --- OPTION 1: FILE UPLOAD ---
st.subheader("Option 1: Upload CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df_upload = pd.read_csv(uploaded_file)
        # Force grab only the first 2 columns (A and B) to prevent the crash
        st.session_state.data_rows = df_upload.iloc[:, :2].values.tolist()
        st.success(f"Successfully loaded {len(st.session_state.data_rows)} rows from CSV.")
    except Exception as e:
        st.error(f"Error reading CSV: {e}")

# --- OPTION 2: MANUAL PASTE ---
st.subheader("Option 2: Manual Paste from Excel")
paste_area = st.text_area("Paste Excel Rows Here (Ctrl+V)", height=150)

if st.button("Process Pasted Data"):
    if paste_area:
        lines = paste_area.strip().split('\n')
        new_rows = []
        for line in lines:
            parts = line.split('\t')
            # Grab only the first two columns even if Excel sends more
            just = parts[0] if len(parts) > 0 else ""
            cont = parts[1] if len(parts) > 1 else ""
            # Skip the header row if it's included in the paste
            if "Justification" not in just:
                new_rows.append([just, cont])
        
        st.session_state.data_rows = new_rows
        st.success(f"Processed {len(st.session_state.data_rows)} rows from paste.")

# --- THE DATA VIEW (EXCEL MIMIC) ---
if st.session_state.data_rows:
    st.divider()
    st.subheader(f"Current Spreadsheet Data ({len(st.session_state.data_rows)} Rows)")
    
    # Create a DataFrame for the editor
    df_to_edit = pd.DataFrame(st.session_state.data_rows, columns=["Justification", "Content Description"])
    
    # The Data Editor shows ALL rows with a scrollbar
    edited_df = st.data_editor(df_to_edit, use_container_width=True, height=500, num_rows="dynamic")

    # Generate the JSON code from the (potentially edited) table
    final_data = edited_df.values.tolist()
    extension_code = json.dumps(final_data)
    
    st.subheader("Copy this code for the Extension:")
    st.code(extension_code, language="json")
    st.info("Select all text in the black box above, Copy it, and Paste it into your Extension popup.")
