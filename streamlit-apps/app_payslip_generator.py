import streamlit as st
import pandas as pd
import zipfile
from io import BytesIO
from reportlab.lib.pagesizes import letter  # Short Bond Paper (8.5" x 11")
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader

# Function to extract pay period from the first row
def extract_pay_period(file):
    df = pd.read_csv(file, nrows=1, header=None)
    return df.iloc[0, 1] if df.shape[1] > 1 else "Not Specified"

def find_header_row(file):
    df_preview = pd.read_csv(file, header=None, nrows=10)  # Read first 10 rows
    file.seek(0)  # Reset file pointer after reading preview
    
    for i, row in df_preview.iterrows():
        if {"Employee", "Rate", "Total"}.issubset(set(row.dropna().astype(str))):
            return i  # Return the row index where the headers start
    return None

# Custom Payslip Generator
class PayslipGenerator:
    def __init__(self, employee_name, details, pay_period, logo_path="https://raw.githubusercontent.com/Music-Admin/mini-tools/refs/heads/main/streamlit-apps/logo-large.png"):
        self.employee_name = employee_name
        self.details = details
        self.pay_period = pay_period
        self.logo_path = logo_path

    def generate_payslip(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30, bottomMargin=50)  
        elements = []

        styles = getSampleStyleSheet()
        header_style = ParagraphStyle(name="HeaderStyle", fontSize=12, alignment=0, spaceAfter=2)
        right_aligned_style = ParagraphStyle(name="RightAlign", fontSize=12, alignment=2, spaceAfter=2)
        footer_style = ParagraphStyle(name="FooterStyle", fontSize=9, alignment=1, textColor=colors.black)

        # Logo (Maintain Aspect Ratio by Fixing Height Only)
        try:
            logo = ImageReader(self.logo_path)
            iw, ih = logo.getSize()
            aspect_ratio = iw / ih  # Calculate aspect ratio
            logo_image = Image(self.logo_path, width=aspect_ratio * 60, height=60)  # Adjust width dynamically
            elements.append(logo_image)
        except:
            elements.append(Paragraph("Company Logo Not Found", header_style))

        elements.append(Spacer(1, 40))  # Space below logo

        # Employee Info (Left) & Payslip Info (Right)
        employee_text = Paragraph(f"<b>Employee:</b> {self.employee_name}", header_style)
        rate_text = Paragraph(f"<b>Rate:</b> {self.details.get('Rate', 'N/A')}", header_style)

        # Ensure period does not wrap
        pay_period_text = Paragraph(f"<b>Period:</b> {self.pay_period}", right_aligned_style)
        payslip_title = Paragraph("<b>PAYSLIP</b>", right_aligned_style)

        elements.append(Table(
            [[employee_text, payslip_title], [rate_text, pay_period_text]],
            colWidths=[260, 260]
        ))

        elements.append(Spacer(1, 60))  # More space before table

        # Payroll Table (Full-Width)
        data = [["Category", "Amount"]]
        for key, value in self.details.items():
            if key not in ["Employee", "Rate", "Total"]:  # Exclude Employee & Rate from table
                if value != 0:
                    data.append([key, f"${value:.2f}"])

        # Add two blank rows before Total
        data.append(["", ""])
        data.append(["", ""])
        data.append(["Total", f"${self.details.get('Total', 0):.2f}"])

        table = Table(data, colWidths=[370, 150])

        # Alternating Row Colors
        row_count = len(data)
        table_styles = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4167B1")),  # Header in blue
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),  # Header text white
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (-2, -1), (-1, -1), "Helvetica-Bold"),  # Bold for Total
        ]

        # Apply alternating background color to rows
        for i in range(1, row_count - 1):  # Skip header & total
            if i % 2 == 0:
                table_styles.append(("BACKGROUND", (0, i), (-1, i), colors.whitesmoke))
            else:
                table_styles.append(("BACKGROUND", (0, i), (-1, i), colors.lightgrey))

        table.setStyle(TableStyle(table_styles))
        elements.append(table)

        # Push footer to bottom dynamically
        elements.append(Spacer(1, 380 - (row_count * 10)))  

        # Footer (Full-Width Horizontal Line)
        footer_line = Table([[Paragraph("", footer_style)]], colWidths=[600])  # Extends beyond page margins
        footer_line.setStyle(
            TableStyle([("LINEABOVE", (0, 0), (-1, -1), 1.5, colors.HexColor("#4167B1"))])
        )
        elements.append(footer_line)
        elements.append(Spacer(1, 5))

        # Footer Contact Details (Black Text)
        footer_data = [
            [
                Paragraph("https://musicadmin.com/", footer_style),
                Paragraph("hello@musicadmin.com", footer_style),
                Paragraph("615-200-0122", footer_style)
            ]
        ]

        footer_table = Table(
            footer_data,
            colWidths=[173, 173, 173],  # Full width for better alignment
            rowHeights=15
        )
        footer_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ]
            )
        )

        elements.append(footer_table)

        doc.build(elements)
        buffer.seek(0)
        return buffer

# Function to generate a ZIP file containing all PDFs
def generate_zip(df, pay_period):
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for _, row in df.iterrows():
            emp_name = row["Employee"]
            payslip = PayslipGenerator(emp_name, row.to_dict(), pay_period).generate_payslip()
            zip_file.writestr(f"Payslip_{emp_name}.pdf", payslip.read())

    zip_buffer.seek(0)
    return zip_buffer

# Streamlit UI
st.title("Employee Payslip Generator")

uploaded_file = st.file_uploader("Upload Payroll CSV", type=["csv"])

if uploaded_file:
    pay_period = extract_pay_period(uploaded_file)  # Extract pay period
    uploaded_file.seek(0)  # Reset file pointer

    header_row = find_header_row(uploaded_file)
    uploaded_file.seek(0)  # Reset file pointer
    
    df = pd.read_csv(uploaded_file, header=header_row)  # Skip first 2 rows (header row after period)

    # Validate column presence
    required_columns = {"Employee", "Rate", "Total"}
    if not required_columns.issubset(df.columns):
        st.error("CSV must contain at least Employee, Rate, and Total columns.")
    else:
        if st.button("Generate Payslips ZIP"):
            zip_file = generate_zip(df, pay_period)
            st.download_button(
                label="Download All Payslips (ZIP)",
                data=zip_file,
                file_name="Payslips.zip",
                mime="application/zip",
            )
