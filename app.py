import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Dual-Box Bridge", layout="wide")

st.title("Excel-to-Extension: Dual-Box Paste")
st.write("Paste Column A in the first box and Column B in the second box.")

# --- DUAL INPUT BOXES ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Paste Column A (Justification)")
    just_input = st.text_area("Justification data here...", height=300, placeholder="The narration sustains perfectly...")

with col2:
    st.subheader("2. Paste Column B (Content Description)")
    desc_input = st.text_area("Description data here...", height=300, placeholder="The evaluated media presents...")

if just_input and desc_input:
    # Split both inputs into lists
    just_list = [line.strip() for line in just_input.strip().split('\n')]
    desc_list = [line.strip() for line in desc_input.strip().split('\n')]
    
    # Handle Header skipping: If the first line is the title, skip it
    if just_list[0].lower() == "justification": just_list.pop(0)
    if desc_list[0].lower() == "content description": desc_list.pop(0)

    # Combine them into pairs
    combined_data = []
    # Loop based on the shorter list to prevent index errors
    for i in range(min(len(just_list), len(desc_list))):
        combined_data.append([just_list[i], desc_list[i]])

    # --- DISPLAY & PREVIEW ---
    st.divider()
    st.subheader(f"Verification: {len(combined_data)} Rows Ready")
    
    # Show the table so you can see if the text matches your Excel
    preview_df = pd.DataFrame(combined_data, columns=["Justification", "Content Description"])
    st.dataframe(preview_df, use_container_width=True, height=400)

    # Generate Code for Extension
    extension_code = json.dumps(combined_data)
    st.subheader("3. Copy this code for your Extension:")
    st.code(extension_code, language="json")
    
    if len(just_list) != len(desc_list):
        st.warning(f"Note: Column A has {len(just_list)} lines, but Column B has {len(desc_list)} lines.")
else:
    st.info("Waiting for you to paste data into both boxes.")
