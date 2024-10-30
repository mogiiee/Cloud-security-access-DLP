import boto3
import re
import os

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

def search_aws_bucket(query):
    """Search for a query in all files of the S3 bucket."""
    results = []
    try:
        response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
        for obj in response.get("Contents", []):
            obj_body = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=obj["Key"])["Body"].read().decode()
            if query in obj_body:
                matches = extract_sensitive_data(obj_body)
                results.append({"file": obj["Key"], "matches": matches})
    except Exception as e:
        print(f"Error accessing AWS S3: {str(e)}")
    return results

def extract_sensitive_data(text):
    """Extract emails, phone numbers, and SSNs using regex."""
    patterns = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"(\+?\d{1,3})?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    }
    matches = {}
    for label, pattern in patterns.items():
        found = re.findall(pattern, text)
        if found:
            matches[label] = found
    return matches