from google.cloud import storage
import json
import os
import re
from fuzzywuzzy import fuzz

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_access_token.json"
GCP_BUCKET_NAME = "large_data_bucket"

# Initialize the GCP Storage client
storage_client = storage.Client()

# Define regex patterns for various data types
patterns = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "phone": r"(\+?\d{1,3})?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
    "address": r"\d{1,5}\s\w+(\s\w+){1,}",
}

def search_gcp_bucket(query):
    """Search for a query in all files of the GCP bucket using fuzzy matching and regex patterns."""
    results = []
    bucket = storage_client.get_bucket(GCP_BUCKET_NAME)
    
    for blob in bucket.list_blobs():
        # Download and parse the JSON content
        content = blob.download_as_text()
        records = json.loads(content)
        
        # Check each record for a match using fuzzy matching
        for record in records:
            if is_fuzzy_match(record, query) or contains_regex_patterns(record):
                results.append({"source": "GCP", "file": blob.name, "record": record})
    return results

def is_fuzzy_match(record, query, threshold=85):
    """Check if any value in the record approximately matches the query using fuzzy matching."""
    for value in record.values():
        if isinstance(value, str) and fuzz.ratio(value.lower(), query.lower()) >= threshold:
            return True
    return False

def contains_regex_patterns(record):
    """Check if any value in the record matches complex regex patterns."""
    for value in record.values():
        if isinstance(value, str):
            for pattern_name, pattern in patterns.items():
                if re.search(pattern, value):
                    return True
    return False