from fastapi import FastAPI
from backend.db import db
from backend.models import PublicResource, DLPViolation
from backend.cloud_integrations.aws import get_public_s3_buckets
from backend.cloud_integrations.gcp import get_public_gcp_buckets

app = FastAPI()

@app.get("/aws/public-buckets")
async def aws_public_buckets():
    buckets = get_public_s3_buckets()
    return {"public_buckets": buckets}

@app.get("/gcp/public-buckets")
async def gcp_public_buckets():
    buckets = get_public_gcp_buckets()
    return {"public_buckets": buckets}

@app.post("/dlp/violations")
async def report_dlp_violation(violation: DLPViolation):
    result = await db["dlp_violations"].insert_one(violation.dict())
    return {"id": str(result.inserted_id)}