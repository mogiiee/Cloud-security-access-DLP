import boto3
import json
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
        # List all objects in the bucket
        response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)
        
        for obj in response.get("Contents", []):
            # Retrieve object content
            obj_body = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=obj["Key"])["Body"].read().decode()
            records = json.loads(obj_body)

            # Check each record for a match
            for record in records:
                if any(query.lower() in str(value).lower() for value in record.values()):
                    results.append({"source": "AWS", "file": obj["Key"], "record": record})
    except Exception as e:
        print(f"Error accessing AWS S3: {str(e)}")
    return results