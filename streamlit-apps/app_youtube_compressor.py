import streamlit as st
import pandas as pd
from io import BytesIO

# Set page config
st.set_page_config(page_title="Royalty Report Compressor", page_icon="📂", layout="wide")

# Custom CSS for full centering
st.markdown(
    """
    <style>
        /* Center the whole page */
        .main { display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column; }
        
        /* Center title */
        h1 { text-align: center; color: #ff6600; font-size: 36px; }

        /* Center subtitle text */
        .subtitle { text-align: center; font-size: 18px; color: #444; margin-top: -10px; margin-bottom: -20px; }

        /* Center file uploader */
        .file-uploader-container { display: flex; justify-content: center; width: 100%; align: center; }
        .stFileUploader { max-width: 500px !important; margin: auto; }

        /* Center download button */
        .stDownloadButton { display: flex; justify-content: center; }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1>Royalty Report Compressor</h1>", unsafe_allow_html=True)

# Centered Subtitle Text
st.markdown(
    '<p class="subtitle">Upload your YouTube raw financial reports to get them compressed and ready for seamless ingestion into the Music Maestro software.</p>',
    unsafe_allow_html=True
)

# Centered File Upload Box
st.markdown('<div class="file-uploader-container">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["csv"])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    # Read CSV with "Adjustment Type" as string
    df = pd.read_csv(uploaded_file)

    if "Adjustment Type" in df.columns:
        df["Adjustment Type"] = df["Adjustment Type"].fillna("None").astype(str)

    # Store original column order
    original_columns = df.columns.tolist()

    # Columns to sum
    sum_columns = [
        "Owned Views", "YouTube Revenue Split : Auction", "YouTube Revenue Split : Reserved",
        "YouTube Revenue Split : Partner Sold YouTube Served", "YouTube Revenue Split : Partner Sold Partner Served",
        "YouTube Revenue Split", "Partner Revenue : Auction", "Partner Revenue : Reserved",
        "Partner Revenue : Partner Sold YouTube Served", "Partner Revenue : Partner Sold Partner Served",
        "Partner Revenue"
    ]

    # Identify non-numeric columns (excluding Asset ID, since we're grouping by it)
    non_numeric_columns = [col for col in original_columns if col not in sum_columns and col != "Asset ID"]

    # Convert numeric columns to float and handle missing values
    df[sum_columns] = df[sum_columns].apply(pd.to_numeric, errors="coerce").fillna(0)

    # Group by Asset ID, sum numeric columns, and retain first value of non-numeric columns
    df = df.groupby("Asset ID", as_index=False).agg(
        {**{col: "sum" for col in sum_columns}, **{col: "first" for col in non_numeric_columns}}
    )

    # Ensure original column order is preserved
    df = df[original_columns]

    # Convert to CSV
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # Extract original file name without extension
    original_filename = uploaded_file.name.rsplit(".", 1)[0]
    compressed_filename = f"[COMPRESSED] {original_filename}.csv"

    # Centered Download Button
    st.markdown('<div class="download-container">', unsafe_allow_html=True)
    st.download_button("Download Compressed Report", output, file_name=compressed_filename, mime="text/csv")
    st.markdown("</div>", unsafe_allow_html=True)