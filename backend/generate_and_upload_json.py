import boto3
import json
import os
from faker import Faker

# Initialize the Faker library to generate fake data
fake = Faker()

# Load AWS credentials from environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# Initialize the S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

def generate_large_json_file(file_name, num_records=100000):
    """Generate a JSON file with a specified number of fake records."""
    data = []

    for _ in range(num_records):
        record = {
            "name": fake.name(),
            "phone_number": fake.phone_number(),
            "address": fake.address(),
            "ssn": fake.ssn(),
            "job": fake.job(),
            "email": fake.email(),
            "card_number": fake.credit_card_number(),
        }
        data.append(record)

    # Save the data to a local JSON file
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)
    print(f"{num_records} records generated and saved to {file_name}.")

def upload_file_to_s3(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket."""
    if object_name is None:
        object_name = file_name  # Use the same file name as the object name in S3

    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"File {file_name} uploaded to {bucket_name} as {object_name}.")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")

if __name__ == "__main__":
    # Generate a large JSON file with 100,000 records
    json_file_name = "large_data.json"
    generate_large_json_file(json_file_name, num_records=10000)



