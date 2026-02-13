import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Excel Formatter", layout="wide")

st.title("Excel-to-Extension Direct Bridge")
st.write("Paste your Excel columns here, then copy the code for the extension.")

# 1. Direct Paste Area
paste_area = st.text_area("Paste Excel Rows Here", height=250, placeholder="Justification [Tab] Content Description")

if paste_area:
    # Logic to handle Excel's tab-separated copy/paste format
    lines = paste_area.strip().split('\n')
    rows = [line.split('\t') for line in lines]
    
    # Ensure 2 columns: Column A (Justification) and Column B (Description)
    cleaned = [r if len(r) == 2 else [r[0], ""] for r in rows]
    
    # Show the user what they pasted to be sure
    st.subheader("Preview of your data:")
    df = pd.DataFrame(cleaned, columns=["Justification", "Content Description"])
    st.table(df)

    # Convert to the special code for the extension
    extension_code = json.dumps(cleaned)
    
    st.subheader("Copy this code for the Extension:")
    st.code(extension_code, language="json")
    st.success("Step 1: Copy the text above. Step 2: Paste it into the extension popup.")
