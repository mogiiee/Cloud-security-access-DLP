import streamlit as st
import requests
import pandas as pd

# Set up the page layout and title
st.set_page_config(page_title="Cloud Data Loss Prevention (DLP) Tool", layout="wide")

# Title and description
st.title("🔍 Cloud Data Loss Prevention (DLP) Tool")
st.markdown("""
Welcome to the **Cloud Data Loss Prevention (DLP) Tool**! This application scans across **AWS S3** and **GCP Storage** 
for sensitive data, identifying potential data risks and compliance issues.  
Simply enter a **name**, **email**, **phone number**, or any search term, and the tool will search the cloud to retrieve matching records.  
For each match, you'll see **source information** (AWS or GCP), **file name**, and **relevant data fields** like emails, phone numbers, addresses, and more!
""")

# Input field for search term and email option
st.markdown("### 🔍 Search Options")
query = st.text_input("Enter a search term (e.g., name, email, phone number):", "")
request_email = st.checkbox("Send results to email")
user_email = st.text_input("Enter your email address:") if request_email else None
search_button = st.button("Search")

# Perform search and handle user input
if search_button and query:
    with st.spinner("🔍 Searching AWS and GCP buckets..."):
        try:
            # Prepare the backend URL
            backend_url = f"https://cloud-data-backend.onrender.com/search/?query={query}"
            if user_email:
                backend_url += f"&email={user_email}"

            # Optimized API request to deployed backend
            response = requests.get(backend_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Display results or email confirmation
            if "results" in data:
                st.success(f"Search completed! {len(data['results'])} results found.")
                results_list = [
                    {**result["record"], "Source": result["source"], "File": result["file"]}
                    for result in data["results"]
                ]
                results_df = pd.DataFrame(results_list)
                st.dataframe(results_df)
            elif "message" in data:
                if request_email and user_email:
                    st.success(f"Results have been sent to {user_email}.")
                else:
                    st.info(data["message"])
            else:
                st.warning("No matching results found in AWS or GCP buckets.")
        
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {str(e)}")

# Additional informational sections for guidance
st.markdown("---")
st.markdown("### 💡 How It Works")
st.markdown("""
- **Data Sources**: This tool searches across both **AWS S3** and **GCP Storage** buckets for sensitive data.
- **Regex Search**: It uses regular expressions to identify sensitive data patterns like **names**, **emails**, **phone numbers**, **SSNs**, **job titles**, and **credit card numbers**.
- **Source Identification**: Each result clearly shows whether the data was retrieved from AWS or GCP, along with the filename for easy reference.
- **Email Option**: Enable the email option to receive results directly in your inbox for secure access.
""")