import streamlit as st
import pandas as pd
import io

def split_composer_names(df):
    updated_df = df.copy()  # Copy original DataFrame
    column_positions = {}

    # Identify "Composer x Name" columns
    for idx, col in enumerate(df.columns):
        if "Composer" in col and "Name" in col:
            composer_number = col.split()[1]  # Extract composer number (e.g., "1", "2", etc.)
            column_positions[col] = idx  # Store original position

    # Process each Composer column and insert new columns
    for col, idx in sorted(column_positions.items(), key=lambda x: x[1], reverse=True):
        composer_number = col.split()[1]
        expanded_values = df[col].apply(split_name).apply(pd.Series)
        expanded_values.columns = [
            f"Composer {composer_number} First Name",
            f"Composer {composer_number} Middle Name",
            f"Composer {composer_number} Last Name"
        ]

        # Insert new columns in the correct position
        for i, new_col in enumerate(expanded_values.columns):
            updated_df.insert(idx + i, new_col, expanded_values.iloc[:, i])

        # Drop the original "Composer x Name" column
        updated_df.drop(columns=[col], inplace=True)

    return updated_df

def split_name(name):
    if pd.isna(name) or name.strip() == "":
        return "", "", ""
    
    parts = name.split()
    if len(parts) == 2:
        return parts[0], "", parts[1]  # First Name, Empty Middle Name, Last Name
    elif len(parts) > 2:
        return parts[0], parts[1], " ".join(parts[2:])  # First Name, Middle Name, Last Name
    else:
        return name, "", ""  # Only First Name, others empty

# Streamlit UI
st.title("🎵 Composer Name Splitter")
st.write("Upload an Excel or CSV file, and we'll split `Composer x Name` into `First Name`, `Middle Name`, and `Last Name`.")

# File upload
uploaded_file = st.file_uploader("Upload a file", type=["xlsx", "csv"])

if uploaded_file:
    file_name = uploaded_file.name

    # Read the file
    if file_name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    elif file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    st.write("### Preview of Uploaded File")
    st.dataframe(df.head())

    # Process the file
    processed_df = split_composer_names(df)

    # Convert to Excel for download
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        processed_df.to_excel(writer, index=False)
    output.seek(0)

    st.write("### Preview of Processed File")
    st.dataframe(processed_df.head())

    # Download button
    st.download_button(
        label="📥 Download Processed File",
        data=output,
        file_name="processed_composers.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )