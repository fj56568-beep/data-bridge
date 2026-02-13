import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Excel Formatter", layout="wide")

st.title("Excel-to-Extension Direct Bridge")
st.write("Choose your method below to prepare data for the extension.")

# Initialize data variable
data_rows = []

# --- OPTION 1: FILE UPLOAD ---
st.subheader("Option 1: Upload CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read CSV, skip the first row (A1/B1)
    df = pd.read_csv(uploaded_file)
    data_rows = df.values.tolist()
    st.success(f"Loaded {len(data_rows)} rows from file (Skipped Header).")

# --- OPTION 2: MANUAL PASTE ---
st.subheader("Option 2: Manual Paste from Excel")
paste_area = st.text_area("Paste Excel Rows Here (Ctrl+V)", height=150, placeholder="Justification [Tab] Content Description")

if st.button("Process Pasted Data"):
    if paste_area:
        lines = paste_area.strip().split('\n')
        # Handle tab-separation from Excel
        rows = [line.split('\t') for line in lines]
        # Ensure 2 columns and remove any header if accidentally pasted
        data_rows = [r if len(r) == 2 else [r[0], ""] for r in rows if "Justification" not in r[0]]
        st.success(f"Processed {len(data_rows)} pasted rows.")

# --- OUTPUT SECTION ---
if data_rows:
    st.divider()
    st.subheader("Preview of Data")
    preview_df = pd.DataFrame(data_rows, columns=["Justification", "Content Description"])
    st.table(preview_df.head(10)) # Show first 10 rows

    # Convert to the JSON code the extension needs
    extension_code = json.dumps(data_rows)
    
    st.subheader("Copy this code for the Extension:")
    st.code(extension_code, language="json")
    st.info("Select all text in the box above, Copy it, and Paste it into the Extension popup.")
