import logging
from fastapi import FastAPI, HTTPException, Query
from backend.cloud_integrations.aws import search_aws_bucket
from backend.cloud_integrations.gcp import search_gcp_bucket

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/search/")
async def search_data(query: str = Query(..., description="Search term")):
    """Search for a term in both AWS and GCP buckets."""
    try:
        logger.debug(f"Starting search for query: {query}")
        aws_results = search_aws_bucket(query)
        logger.debug(f"AWS results: {aws_results}")
        
        gcp_results = search_gcp_bucket(query)
        logger.debug(f"GCP results: {gcp_results}")
        
        combined_results = aws_results + gcp_results
        logger.debug(f"Combined results: {combined_results}")
        
        if combined_results:
            return {"results": combined_results}
        else:
            return {"message": "No matches found for the given query."}
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")