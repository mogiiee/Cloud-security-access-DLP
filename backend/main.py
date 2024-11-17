import os
from fastapi import FastAPI, HTTPException, Query
from backend.cloud_integrations.aws import search_aws_bucket
from backend.cloud_integrations.gcp import search_gcp_bucket
from mailjet_rest import Client

# Mailjet API credentials
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_API_SECRET = os.getenv("MAILJET_API_SECRET")
SENDER_EMAIL = "your-email@example.com"  # Replace with your verified sender email

app = FastAPI()

def send_email_with_mailjet(to_email, subject, text):
    """Send an email using Mailjet API."""
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
    result = mailjet.send.create(data=data)
    if result.status_code != 200:
        raise Exception(f"Failed to send email: {result.json()}")
    return result.json()

@app.get("/search/")
async def search_data(query: str = Query(..., description="Search term"), email: str = Query(None, description="Optional email address to send results")):
    """Search for a term in both AWS and GCP buckets and optionally email results."""
    try:
        # Fetch results from both AWS and GCP
        aws_results = search_aws_bucket(query)
        gcp_results = search_gcp_bucket(query)

        # Combine results and prepare response
        combined_results = aws_results + gcp_results
        result_message = "No matches found for the given query." if not combined_results else f"{len(combined_results)} results found."

        # If email is provided, send results via email
        if email:
            email_text = "\n\n".join([f"Source: {result['source']}\nFile: {result['file']}\nData: {result['record']}" for result in combined_results])
            email_body = f"Search results for '{query}':\n\n" + (email_text if combined_results else "No matches found.")
            send_email_with_mailjet(email, f"Search Results for '{query}'", email_body)
            return {"message": f"Results emailed to {email}."}

        # Return results in JSON format for regular requests
        return {"results": combined_results} if combined_results else {"message": result_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")