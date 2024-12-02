import streamlit as st
import requests
import pandas as pd

# Set up the page layout and title
st.set_page_config(page_title="Cloud Data Loss Prevention (DLP) Tool", layout="wide")

# Login logic
def login():
    """Login page to restrict access."""
    st.title("🔒 Login")
    st.markdown("Please enter your credentials to access the Cloud DLP Tool.")
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    login_button = st.button("Login")

    if login_button:
        if username == "admin" and password == "admin":
            st.success("Login successful!")
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid username or password.")

# Protect the app with a login page
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
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
    user_email = st.text_input("Enter your email address (required):", "")
    search_button = st.button("Search")

    # Validate that both fields are filled
    if search_button:
        if not query:
            st.error("Please enter a search term.")
        elif not user_email:
            st.error("Please enter a valid email address.")
        else:
            with st.spinner("🔍 Searching all the public AWS and GCP buckets in the internet..."):
                try:
                    # Prepare the backend URL
                    backend_url = f"https://cloud-data-backend.onrender.com/search/?query={query}&email={user_email}"

                    # Optimized API request to deployed backend
                    response = requests.get(backend_url, timeout=10000)
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
                        st.info(f"The results have also been emailed to {user_email}.")
                    elif "message" in data:
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
    - **Email Option**: The results are emailed to the user for secure access.
    """)