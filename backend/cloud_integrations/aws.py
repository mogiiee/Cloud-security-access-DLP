    
import boto3
from backend.config import AWS_ACCESS_KEY, AWS_SECRET_KEY

client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

def get_public_s3_buckets():
    response = client.list_buckets()
    public_buckets = []
    for bucket in response.get("Buckets", []):
        acl = client.get_bucket_acl(Bucket=bucket["Name"])
        for grant in acl["Grants"]:
            if grant["Permission"] == "READ" and grant["Grantee"].get("URI") == "http://acs.amazonaws.com/groups/global/AllUsers":
                public_buckets.append(bucket["Name"])
    return public_buckets