from google.cloud import storage
import json
import os

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/amogharya/Documents/projects/CASB/gcp_access_token.json"
GCP_BUCKET_NAME = "large_data_bucket"

# Initialize the GCP Storage client
storage_client = storage.Client()

def search_gcp_bucket(query):
    """Search for a query in all files of the GCP bucket."""
    results = []
    bucket = storage_client.get_bucket(GCP_BUCKET_NAME)
    
    for blob in bucket.list_blobs():
        # Download and parse the JSON content
        content = blob.download_as_text()
        records = json.loads(content)
        
        # Check each record for a match
        for record in records:
            if any(query.lower() in str(value).lower() for value in record.values()):
                results.append({"source": "GCP", "file": blob.name, "record": record})
    return results