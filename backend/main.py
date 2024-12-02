import os
import logging
from fastapi import FastAPI, HTTPException, Query
from backend.cloud_integrations.aws import search_aws_bucket
from backend.cloud_integrations.gcp import search_gcp_bucket
from mailjet_rest import Client

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Mailjet API credentials
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_API_SECRET = os.getenv("MAILJET_API_SECRET")
SENDER_EMAIL = "amogharya2@gmail.com"  # Replace with your verified sender email

RESULT_LIMIT = 55  # Limit results to 55 items

app = FastAPI()

def send_email_with_mailjet(to_email, subject, text):
    """Send an email using Mailjet API."""
    try:
        logger.debug("Initializing Mailjet client.")
        mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": SENDER_EMAIL,
                        "Name": "Cloud DLP Tool"
                    },
                    "To": [
                        {
                            "Email": to_email,
                            "Name": to_email.split('@')[0]
                        }
                    ],
                    "Subject": subject,
                    "TextPart": text
                }
            ]
        }
        logger.debug("Sending email via Mailjet.")
        result = mailjet.send.create(data=data)
        logger.debug(f"Mailjet response status: {result.status_code}")
        logger.debug(f"Mailjet response body: {result.json()}")
        if result.status_code != 200:
            raise Exception(f"Failed to send email: {result.json()}")
        return result.json()
    except Exception as e:
        logger.exception("An error occurred while sending email.")
        raise

@app.get("/search/")
async def search_data(query: str = Query(..., description="Search term"), email: str = Query(None, description="Optional email address to send results")):
    """Search for a term in both AWS and GCP buckets and optionally email results."""
    try:
        logger.debug(f"Starting search for query: {query}")

        # Fetch results from AWS and GCP
        aws_results = search_aws_bucket(query)
        gcp_results = search_gcp_bucket(query)

        # Combine and limit results
        combined_results = aws_results + gcp_results
        logger.debug(f"Total combined results before limiting: {len(combined_results)}")
        limited_results = combined_results[:RESULT_LIMIT]
        logger.debug(f"Total results after limiting: {len(limited_results)}")

        # If email is provided, send results via email
        if email:
            logger.debug(f"Preparing to email results to {email}.")
            email_text = "\n\n".join([f"Source: {result['source']}\nFile: {result['file']}\nData: {result['record']}" for result in limited_results])
            email_body = f"Search results for '{query}':\n\n" + (email_text if limited_results else "No matches found.")
            send_email_with_mailjet(email, f"Search Results for '{query}'", email_body)
            return {"message": f"Results emailed to {email}."}

        # Return limited results in JSON format
        result_message = "No matches found for the given query." if not limited_results else f"{len(limited_results)} results found."
        return {"results": limited_results} if limited_results else {"message": result_message}
    except Exception as e:
        logger.exception("An error occurred while processing the request.")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")