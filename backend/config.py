import os

MONGO_URI = os.getenv(
    "MONGO_URI", 
    "mongodb+srv://<username>:<password>@cluster0.mongodb.net/cloud_security?retryWrites=true&w=majority"
)

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "")
GCP_CREDENTIALS = os.getenv("GCP_CREDENTIALS", "path/to/credentials.json")