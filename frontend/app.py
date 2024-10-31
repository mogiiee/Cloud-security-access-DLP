import streamlit as st
import requests
import pandas as pd

# Set up the page layout and title
st.set_page_config(page_title="Cloud Data Search Tool", layout="wide")

# Title and description with emojis for enhanced UX
st.title("🔍 Cloud Data Search Tool")
st.markdown("""
Welcome to the **Cloud Data Search Tool**! This app allows you to search through data stored in **AWS S3** and **GCP Storage**.  
Simply enter a **name**, **email**, **phone number**, or any search term, and the tool will scan across both platforms to retrieve matching records.  
For each match, you'll see **source information** (AWS or GCP), **file name**, and **relevant data fields** like emails, phone numbers, addresses, and more!
""")

# Instructions for users on how to use the tool
st.markdown("### 🔍 How to Use")
st.markdown("""
1. **Enter a Search Term**: Type a name, email, or any identifier in the search bar.
2. **Click Search**: The tool will query AWS and GCP for data matching your term.
3. **View Results**: See each matching record with details and source information.
""")

# Input field for search term
query = st.text_input("Enter a search term (e.g., name, email, phone number):", "")
search_button = st.button("Search")

# Perform search and handle user input
if search_button and query:
    with st.spinner("🔍 Searching AWS and GCP buckets..."):
        try:
            # API request to search data
            response = requests.get(f"http://localhost:8000/search/?query={query}")
            response.raise_for_status()
            data = response.json()

            if "results" in data:
                st.success(f"Search completed! {len(data['results'])} results found.")

                # Display results with source and file information in an organized table format
                st.subheader("Search Results")
                results_list = []
                for result in data["results"]:
                    record = result["record"]
                    record["Source"] = result["source"]
                    record["File"] = result["file"]
                    results_list.append(record)
                
                # Convert results to DataFrame for better visualization
                results_df = pd.DataFrame(results_list)
                st.dataframe(results_df)
            else:
                st.warning("No matching results found in AWS or GCP buckets.")
        
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {str(e)}")

# Add informational section about how the search works
st.markdown("---")
st.markdown("### 💡 How It Works")
st.markdown("""
- **Data Sources**: This app searches across both **AWS S3** and **GCP Storage** buckets.
- **Regex Search**: It uses regex to locate matching terms in data fields such as **name**, **phone number**, **email**, **SSN**, **job title**, and **credit card number**.
- **Source Identification**: Each result clearly shows whether the data was retrieved from AWS or GCP, along with the filename for easy reference.
""")

# Include a sample output and explanation of each field in the output
st.markdown("### 📊 Sample Output")
sample_output = {
    "Source": "AWS",
    "File": "sample_data.json",
    "Name": "John Doe",
    "Email": "john.doe@example.com",
    "Phone Number": "+1-555-123-4567",
    "Address": "123 Main St, City, State, ZIP",
    "SSN": "123-45-6789",
    "Job": "Software Engineer",
    "Card Number": "4111 1111 1111 1111"
}
st.json(sample_output)

# Footer and contact information
st.markdown("---")
st.markdown("👨‍💻 **Cloud Data Search Tool** by [Your Name](mailto:your-email@example.com)")