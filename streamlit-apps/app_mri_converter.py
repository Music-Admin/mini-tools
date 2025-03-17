import streamlit as st
import pandas as pd
from io import BytesIO

# Set page config
st.set_page_config(page_title="MuMa to MRI Converter", page_icon="📂", layout="wide")

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
st.markdown("<h1>MuMa to MRI Converter</h1>", unsafe_allow_html=True)

# Centered Subtitle Text
st.markdown(
    '<p class="subtitle">Upload your MuMa ready ingest files to convert them into the MRI Song Delivery format.</p>',
    unsafe_allow_html=True
)

# Centered File Upload Box
st.markdown('<div class="file-uploader-container">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["csv"])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    # Read CSV with "Adjustment Type" as string
    df = pd.read_csv(uploaded_file, dtype=str).fillna("")

    # Storage for formatted rows
    formatted_rows = []

    # Process each row
    for _, row in df.iterrows():
        # Writers & Uncontrolled Writers (strip whitespace)
        i = 1
        while f"Recording {i} Display Artist" in row and row[f"Recording {i} Display Artist"] != "":
            song_data = {"SONG TITLE*": row["Song Title"],
                    "AKA TITLE": "",
                    "MRI SONG ID": "",
                    "PUBLISHER'S SONG ID": "",
                    "ISWC": ""}
            
            if f"Composer {i} Surname" in row:
                song_data["COMPOSER LAST NAME*"] = row[f"Composer {i} Surname"]
                song_data["COMPOSER FIRST NAME*"] = row[f"Composer {i} First Name"]
                song_data["COMPOSER MIDDLE NAME"] = row[f"Composer {i} Middle Name"]
                song_data["COMPOSER PRO"] = ""
                song_data["COMPOSER IPI NUMBER"] = ""
                song_data["CONTROLLED COMPOSER (Y/N)*"] = row[f"Composer {i} Controlled"]
                song_data["COMPOSER SHARE %*"] = row[f"Composer {i} Share"]
                song_data["COMPOSER ROLE CODE"] = row[f"Composer {i} Capacity"]
            else:
                song_data["COMPOSER LAST NAME*"] = ""
                song_data["COMPOSER FIRST NAME*"] = ""
                song_data["COMPOSER MIDDLE NAME"] = ""
                song_data["COMPOSER PRO"] = ""
                song_data["COMPOSER IPI NUMBER"] = ""
                song_data["CONTROLLED COMPOSER (Y/N)*"] = ""
                song_data["COMPOSER SHARE %*"] = ""
                song_data["COMPOSER ROLE CODE"] = ""

            if f"Publisher {i} Name" in row:
                song_data["PUBLISHER NAME *"] = row[f"Publisher {i} Name"]
                song_data["PUBLISHER PRO*"] = ""
                song_data["PUBLISHER IPI NUMBER *"] = ""
                song_data["CONTROLLED PUBLISHER (Y/N)*"] = row[f"Publisher {i} Controlled"]
            else:
                song_data["PUBLISHER NAME *"] = ""
                song_data["PUBLISHER PRO*"] = ""
                song_data["PUBLISHER IPI NUMBER *"] = ""
                song_data["CONTROLLED PUBLISHER (Y/N)*"] = ""
                
            if f"Client {i} Name" in row:
                song_data["ADMINISTRATOR NAME"] = row[f"Client {i} Name"]
                song_data["SHARE %*"] = row[f"Publisher {i} Share"]
                song_data["TERRITORY CONTROLLED*"] = row[f"Territory {i} Name"]
                song_data["TERRITORY EXCLUSIONS (OPTIONAL)"] = ""
                song_data["PUBLISHER MAILING ADDRESS*"] = ""
                song_data["PUBLISHER CONTACT*"] = ""
            else:
                song_data["ADMINISTRATOR NAME"] = ""
                song_data["SHARE %*"] = ""
                song_data["TERRITORY CONTROLLED*"] = ""
                song_data["TERRITORY EXCLUSIONS (OPTIONAL)"] = ""
                song_data["PUBLISHER MAILING ADDRESS*"] = ""
                song_data["PUBLISHER CONTACT*"] = ""

            if f"Recording {i} Display Artist" in row:
                song_data["RECORDING ARTIST NAME"] = row[f"Recording {i} Display Artist"]
                song_data["RECORDING LABEL"] = row[f"Recording {i} Label Name"]
                song_data["RECORDING ISRC"] = row[f"Recording {i} ISRC"]
                song_data["UPC/EAN"] = row[f"Recording {i} UPC"]
            else:
                song_data["RECORDING ARTIST NAME"] = ""
                song_data["RECORDING LABEL"] = ""
                song_data["RECORDING ISRC"] = ""
                song_data["UPC/EAN"] = ""

            formatted_rows.append(song_data)
            i += 1

    # Convert list of dictionaries to DataFrame
    formatted_df = pd.DataFrame(formatted_rows)

    # Convert to CSV
    output = BytesIO()
    formatted_df.to_csv(output, index=False)
    output.seek(0)

    # Extract original file name without extension
    original_filename = uploaded_file.name.rsplit(".", 1)[0]
    compressed_filename = f"[MRI FORMAT] {original_filename}.csv"

    # Centered Download Button
    st.markdown('<div class="download-container">', unsafe_allow_html=True)
    st.download_button("Download Compressed Report", output, file_name=compressed_filename, mime="text/csv")
    st.markdown("</div>", unsafe_allow_html=True)