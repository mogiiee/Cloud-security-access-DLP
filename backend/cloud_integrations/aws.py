import boto3
import json
import os
import re
from fuzzywuzzy import fuzz

# Load AWS credentials from environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

# Define complex regex patterns for various data types
patterns = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "phone": r"(\+?\d{1,3})?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
    "address": r"\d{1,5}\s\w+(\s\w+){1,}",
}

def search_aws_bucket(query):
    """Search for a query in all files of the S3 bucket using fuzzy matching and regex patterns."""
    results = []
    try:
        # List all objects in the bucket
        response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
        
        for obj in response.get("Contents", []):
            # Retrieve object content
            obj_body = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=obj["Key"])["Body"].read().decode()
            records = json.loads(obj_body)

            # Check each record for a match using fuzzy matching
            for record in records:
                if is_fuzzy_match(record, query) or contains_regex_patterns(record):
                    results.append({"source": "AWS", "file": obj["Key"], "record": record})
    except Exception as e:
        print(f"Error accessing AWS S3: {str(e)}")
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