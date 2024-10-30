from google.cloud import storage
import re
from backend.config import GCP_CREDENTIALS

client = storage.Client.from_service_account_json(GCP_CREDENTIALS)

def search_gcp_bucket(bucket_name, query):
    results = []
    bucket = client.get_bucket(bucket_name)
    for blob in bucket.list_blobs():
        content = blob.download_as_text()
        if query in content:
            results.extend(extract_sensitive_data(content))
    return results

def extract_sensitive_data(text):
    patterns = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"(\+?\d{1,3})?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    }
    matches = []
    for label, pattern in patterns.items():
        matches.extend(re.findall(pattern, text))
    return matches