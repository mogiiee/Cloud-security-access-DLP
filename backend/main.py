from fastapi import FastAPI, HTTPException, Query
from backend.cloud_integrations.aws import search_aws_bucket
from backend.cloud_integrations.gcp import search_gcp_bucket

app = FastAPI()

@app.get("/search/")
async def search_data(query: str = Query(..., description="Search term")):
    """Efficiently search for a term in both AWS and GCP buckets."""
    try:
        # Fetch results from both AWS and GCP
        aws_results = search_aws_bucket(query)
        gcp_results = search_gcp_bucket(query)

        # Combine results and respond
        combined_results = aws_results + gcp_results
        return {"results": combined_results} if combined_results else {"message": "No matches found for the given query."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve data.")