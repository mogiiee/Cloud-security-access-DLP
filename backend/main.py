from fastapi import FastAPI, HTTPException
from backend.cloud_integrations.aws import search_aws_bucket
from backend.cloud_integrations.gcp import search_gcp_bucket

app = FastAPI()

AWS_BUCKET_NAME = "your-aws-bucket-name"
GCP_BUCKET_NAME = "your-gcp-bucket-name"

@app.get("/search/")
async def search_data(query: str):
    try:
        aws_results = search_aws_bucket(AWS_BUCKET_NAME, query)
        gcp_results = search_gcp_bucket(GCP_BUCKET_NAME, query)
        return {"aws_results": aws_results, "gcp_results": gcp_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))