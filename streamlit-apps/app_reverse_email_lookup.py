import streamlit as st
import requests
from dotenv import load_dotenv
import os

# --- Load API Key ---
load_dotenv()
PDL_API_KEY = os.getenv("PDL_API_KEY") or st.secrets["PDL_API_KEY"]

# --- UI ---
st.set_page_config(page_title="PDL Email Lookup", layout="wide")
st.title("🔍 Reverse Email Lookup (People Data Labs)")

email = st.text_input("Enter email address")

def safe_get(data, path, default=None):
    for key in path.split("."):
        data = data.get(key, {})
    return data or default

if st.button("Lookup"):
    if not email:
        st.warning("Please enter an email address.")
    else:
        with st.spinner("Looking up info..."):
            PARAMS = {
                "api_key": PDL_API_KEY,
                "email": email
            }
            response = requests.get(
                "https://api.peopledatalabs.com/v5/person/enrich",
                params=PARAMS
            )

            if response.status_code == 200:
                result = response.json()

                if result.get("status") == 404 or not result.get("data"):
                    st.info("No match found.")
                else:
                    st.success("✅ Person found!")

                    data = result["data"]  # <- FIXED: Extract actual data

                    # Personal Info
                    st.header("👤 Personal Info")
                    st.write(f"**Full Name**: {data.get('full_name')}")
                    st.write(f"**First Name**: {data.get('first_name')}")
                    st.write(f"**Middle Name**: {data.get('middle_name')}")
                    st.write(f"**Last Name**: {data.get('last_name')}")
                    st.write(f"**Sex**: {data.get('sex')}")
                    st.write(f"**Birth Year**: {data.get('birth_year')}")
                    st.write(f"**Birth Date**: {data.get('birth_date')}")

                    # Contact
                    st.header("📞 Contact Info")
                    st.write(f"**Mobile Phone**: {data.get('mobile_phone')}")
                    st.write(f"**Work Email**: {data.get('work_email')}")
                    st.write(f"**Recommended Personal Email**: {data.get('recommended_personal_email')}")

                    # Location
                    st.header("📍 Location")
                    st.write(f"**Location Name**: {data.get('location_name')}")
                    st.write(f"**Region**: {data.get('location_region')}")
                    st.write(f"**Country**: {data.get('location_country')}")
                    st.write(f"**Street Address**: {data.get('location_street_address')}")
                    st.write(f"**Postal Code**: {data.get('location_postal_code')}")

                    # Social
                    st.header("🔗 Social Profiles")
                    st.write(f"[LinkedIn]({data.get('linkedin_url')})")
                    st.write(f"[Twitter]({data.get('twitter_url')})")
                    st.write(f"[Facebook]({data.get('facebook_url')})")
                    st.write(f"[GitHub]({data.get('github_url')})")

                    # Work Info
                    st.header("🏢 Work Info")
                    st.write(f"**Job Title**: {data.get('job_title')}")
                    st.write(f"**Job Role**: {data.get('job_title_role')}")
                    st.write(f"**Company Name**: {data.get('job_company_name')}")
                    st.write(f"**Company Website**: {data.get('job_company_website')}")
                    st.write(f"**Company Size**: {data.get('job_company_size')}")
                    st.write(f"**Company Industry**: {data.get('job_company_industry')}")
                    st.write(f"[Company LinkedIn]({data.get('job_company_linkedin_url')})")

                    # Experience
                    if "experience" in data:
                        st.header("🧑‍💼 Experience")
                        for i, job in enumerate(data["experience"][:5]):
                            st.subheader(f"{job.get('title')} at {job.get('company_name')}")
                            st.write(f"- Role: {job.get('job_title_role')}")
                            st.write(f"- Location: {job.get('location_name')}")
                            st.write(f"- Start: {job.get('start_date')} | End: {job.get('end_date')}")

                    # Education
                    if "education" in data:
                        st.header("🎓 Education")
                        for edu in data["education"][:5]:
                            st.subheader(edu.get("school"))
                            st.write(f"- Degree: {edu.get('degree')}")
                            st.write(f"- Major: {edu.get('major')}")
                            st.write(f"- Graduation: {edu.get('end_date')}")

            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
