import streamlit as st
import pandas as pd
import json
import re

st.set_page_config(page_title="Excel Range Bridge", layout="wide")

st.title("Excel-to-Extension: Range Selector")
st.write("1. Paste your data. 2. Define your range (e.g., 2:254). 3. Copy the code.")

# 1. Manual Paste Area
pasted_text = st.text_area("Paste Excel Rows Here", height=200)

# 2. Range Input
range_input = st.text_input("Enter Row Range (e.g., 2:254 or leave blank for ALL)", placeholder="2:254")

if pasted_text:
    # Split text into a full list of rows
    all_lines = pasted_text.strip().split('\n')
    all_data = []
    for line in all_lines:
        parts = line.split('\t')
        just = parts[0] if len(parts) > 0 else ""
        desc = parts[1] if len(parts) > 1 else ""
        all_data.append([just, desc])

    # Apply Range Filtering
    final_data = all_data
    if range_input and ":" in range_input:
        try:
            # Extract numbers from format like "A2:A254" or "2:254"
            nums = re.findall(r'\d+', range_input)
            start_row = int(nums[0]) - 1 # Adjust for 0-based indexing
            end_row = int(nums[1])
            final_data = all_data[start_row:end_row]
            st.success(f"Showing Rows {start_row + 1} to {end_row}")
        except Exception:
            st.warning("Range format invalid. Showing all pasted data.")

    # 3. Visual Preview
    st.subheader("Data Preview")
    df = pd.DataFrame(final_data, columns=["Justification", "Content Description"])
    st.dataframe(df, use_container_width=True, height=400)

    # 4. Extension Code
    st.subheader("Copy this code for your Extension:")
    extension_code = json.dumps(final_data)
    st.code(extension_code, language="json")
    
    st.info(f"Total rows ready for extension: {len(final_data)}")
