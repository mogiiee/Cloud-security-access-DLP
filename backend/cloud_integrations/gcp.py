from google.cloud import storage
import json
import os
import re

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_access_token.json"
GCP_BUCKET_NAME = "large_data_bucket"

# Initialize the GCP Storage client
storage_client = storage.Client()

def search_gcp_bucket(query):
    """Search for a query in all files of the GCP bucket using regex matching."""
    results = []
    bucket = storage_client.get_bucket(GCP_BUCKET_NAME)
    
    # Compile a regex pattern for case-insensitive, partial matching
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    for blob in bucket.list_blobs():
        # Download and parse the JSON content
        content = blob.download_as_text()
        records = json.loads(content)
        
        # Check each record for a regex match
        for record in records:
            if has_regex_match(record, pattern):
                results.append({"source": "GCP", "file": blob.name, "record": record})
    return results

def has_regex_match(record, pattern):
    """Check if any relevant field in the record matches the regex pattern."""
    for field in ["name", "email"]:  # Specify fields to target for matching
        if field in record and isinstance(record[field], str) and pattern.search(record[field]):
            return True
    return False