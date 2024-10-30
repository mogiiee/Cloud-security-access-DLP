import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Cloud Data Search", layout="wide")

# Title and description
st.title("🔍 Cloud Data Search Tool")
st.markdown("""
This tool allows you to search **AWS S3** and **GCP Storage Buckets** for specific information, such as:
- **Emails** (e.g., john.doe@example.com)
- **Phone Numbers** (e.g., +1-555-123-4567)
- **Social Security Numbers (SSNs)** (e.g., 123-45-6789)

Simply enter a **name or keyword** below, and the tool will query both AWS and GCP buckets and display all matching results.
""")

# Input field and search button
query = st.text_input("Enter a name or keyword to search:", "")
search_button = st.button("Search")

# Progress indicator and API call
if search_button and query:
    with st.spinner("Searching AWS and GCP buckets..."):
        try:
            response = requests.get(f"http://localhost:8000/search/?query={query}")
            response.raise_for_status()
            data = response.json()

            # Display results
            if data["aws_results"] or data["gcp_results"]:
                st.success("Search completed! Results found.")
                
                # AWS Results
                st.subheader("🗂 AWS S3 Bucket Results")
                if data["aws_results"]:
                    aws_df = pd.DataFrame(data["aws_results"], columns=["Match"])
                    st.dataframe(aws_df)
                else:
                    st.info("No matches found in AWS S3 buckets.")

                # GCP Results
                st.subheader("🗂 GCP Storage Bucket Results")
                if data["gcp_results"]:
                    gcp_df = pd.DataFrame(data["gcp_results"], columns=["Match"])
                    st.dataframe(gcp_df)
                else:
                    st.info("No matches found in GCP Storage buckets.")
            else:
                st.warning("No matching results found in AWS or GCP buckets.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {str(e)}")

# Footer with helpful information
st.markdown("""
---
### How it Works
- The tool queries **AWS S3** and **GCP Storage Buckets** for the keyword you enter.
- It uses **regular expressions (regex)** to detect emails, phone numbers, and SSNs.
- Results are displayed in interactive tables for easier review.

### Example Searches
- Try searching for a **name** like "John".
- Or search for **emails** by entering part of an email (e.g., "example").
""")