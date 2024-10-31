import json
from faker import Faker
from google.cloud import storage
import os

# Initialize the Faker library to generate fake data
fake = Faker()

# Load GCP credentials from the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "backend/generate_and_upload_json.py"

def generate_large_json_file(file_name, num_records=10000):
    """Generate a JSON file with a specified number of fake records."""
    data = []

    for _ in range(num_records):
        record = {
            "name": fake.name(),
            "phone_number": fake.phone_number(),
            "address": fake.address(),
            "ssn": fake.ssn(),
            "email": fake.email(),
            "card_number": fake.credit_card_number(),
            "job": fake.job(),
            
        }
        data.append(record)

    # Save the data to a local JSON file
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)
    print(f"{num_records} records generated and saved to {file_name}.")

def upload_file_to_gcp(bucket_name, file_name, object_name=None):
    """Upload a file to a GCP bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    if object_name is None:
        object_name = file_name  # Use the same file name as the object name in GCP

    blob = bucket.blob(object_name)

    try:
        blob.upload_from_filename(file_name)
        print(f"File {file_name} uploaded to {bucket_name} as {object_name}.")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")

if __name__ == "__main__":
    # Generate a large JSON file with 100,000 records
    json_file_name = "large_data_gcp.json"
    generate_large_json_file(json_file_name, num_records=100000)

    # Upload the generated JSON file to GCP Storage
    upload_file_to_gcp("my-cloud-security-bucket", json_file_name)