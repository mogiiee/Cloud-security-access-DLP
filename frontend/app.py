import streamlit as st
import requests

st.title("Cloud Security Dashboard")

# Fetch AWS public buckets
aws_buckets = requests.get("http://localhost:8000/aws/public-buckets").json()["public_buckets"]
st.subheader("AWS Public Buckets")
st.write(aws_buckets)

# Fetch GCP public buckets
gcp_buckets = requests.get("http://localhost:8000/gcp/public-buckets").json()["public_buckets"]
st.subheader("GCP Public Buckets")
st.write(gcp_buckets)

# DLP Violation Reporting
st.subheader("Report DLP Violation")
with st.form("dlp_form"):
    service = st.text_input("Service")
    data = st.text_area("Data")
    violation_type = st.text_input("Violation Type")
    submitted = st.form_submit_button("Submit")

    if submitted:
        response = requests.post(
            "http://localhost:8000/dlp/violations",
            json={
                "service": service,
                "data": data,
                "violation_type": violation_type,
                "timestamp": "2024-10-28T12:00:00Z"
            },
        )
        st.success(f"Violation reported! ID: {response.json()['id']}")