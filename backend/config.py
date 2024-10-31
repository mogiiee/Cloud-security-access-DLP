import os

MONGO_URI = os.getenv(
    "MONGO_URI", 
    "mongodb+srv://mogiiee:mogiiee@cluster0.f8mil.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "")
GCP_CREDENTIALS = os.getenv("GCP_CREDENTIALS", "path/to/credentials.json")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "cloud-security-bucket-1")  # Default bucket name