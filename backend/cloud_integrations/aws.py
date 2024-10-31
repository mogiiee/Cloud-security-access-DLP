import boto3
import json
import os
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

def search_aws_bucket(query):
    """Search for a query in all files of the S3 bucket using improved matching."""
    results = []
    try:
        # List all objects in the bucket
        response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
        
        for obj in response.get("Contents", []):
            # Retrieve object content
            obj_body = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=obj["Key"])["Body"].read().decode()
            records = json.loads(obj_body)

            # Check each record for a precise fuzzy match
            for record in records:
                if is_precise_fuzzy_match(record, query):
                    results.append({"source": "AWS", "file": obj["Key"], "record": record})
    except Exception as e:
        print(f"Error accessing AWS S3: {str(e)}")
    return results

def is_precise_fuzzy_match(record, query, threshold=85):
    """Check for a high-relevance match based on specific fields in the record."""
    for field in ["name", "email"]:  # Add fields you want to target, such as "name" or "email"
        if field in record and isinstance(record[field], str):
            if fuzz.ratio(record[field].lower(), query.lower()) >= threshold:
                return True
    return False