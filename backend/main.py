import os
import requests
from fastapi import FastAPI, HTTPException, Query
from backend.cloud_integrations.aws import search_aws_bucket
from backend.cloud_integrations.gcp import search_gcp_bucket

# Mailgun settings (replace these with your own)
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
SENDER_EMAIL = f"data-protection@{MAILGUN_DOMAIN}"  # e.g., "data-protection@sandbox1234.mailgun.org"

app = FastAPI()

def send_email(to_email, subject, text):
    """Send an email using Mailgun API."""
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": SENDER_EMAIL,
              "to": to_email,
              "subject": subject,
              "text": text})
    response.raise_for_status()
    return response.json()

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
            send_email(email, f"Search Results for '{query}'", email_body)
            return {"message": f"Results emailed to {email}."}

        # Return results in JSON format for regular requests
        return {"results": combined_results} if combined_results else {"message": result_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve data or send email.")