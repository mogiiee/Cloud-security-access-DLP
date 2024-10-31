from google.cloud import storage
import json
import os
from fuzzywuzzy import fuzz

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_access_token.json"
GCP_BUCKET_NAME = "large_data_bucket"

# Initialize the GCP Storage client
storage_client = storage.Client()

def search_gcp_bucket(query):
    """Search for a query in all files of the GCP bucket using improved matching."""
    results = []
    bucket = storage_client.get_bucket(GCP_BUCKET_NAME)
    
    for blob in bucket.list_blobs():
        # Download and parse the JSON content
        content = blob.download_as_text()
        records = json.loads(content)
        
        # Check each record for a precise fuzzy match
        for record in records:
            if is_precise_fuzzy_match(record, query):
                results.append({"source": "GCP", "file": blob.name, "record": record})
    return results

def is_precise_fuzzy_match(record, query, threshold=85):
    """Check for a high-relevance match based on specific fields in the record."""
    for field in ["name", "email"]:  # Add fields you want to target
        if field in record and isinstance(record[field], str):
            if fuzz.ratio(record[field].lower(), query.lower()) >= threshold:
                return True
    return False