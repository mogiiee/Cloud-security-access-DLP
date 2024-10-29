from google.cloud import storage
from backend.config import GCP_CREDENTIALS

client = storage.Client.from_service_account_json(GCP_CREDENTIALS)

def get_public_gcp_buckets():
    public_buckets = []
    for bucket in client.list_buckets():
        if bucket.iam_configuration.uniform_bucket_level_access_enabled:
            public_buckets.append(bucket.name)
    return public_buckets