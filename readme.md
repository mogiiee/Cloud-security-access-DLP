# Cloud Security Access DLP

## Overview
This Cloud Security Tool is a lightweight cloud monitoring solution designed to help organizations detect and report misconfigurations and potential data security issues in cloud environments. It integrates with **AWS** and **GCP** to identify public resources, misconfigurations, and sensitive data patterns using Data Loss Prevention (DLP). The tool provides a **dashboard interface** built with Streamlit for visualization and easy reporting.

---

## Features
1. **Cloud Integration:**
   - Detect publicly accessible **AWS S3 buckets** and **GCP storage buckets**.
   - Retrieve cloud logs from **AWS CloudTrail** and **GCP Logging** for monitoring.

2. **Data Loss Prevention (DLP):**
   - Scan for sensitive data patterns (e.g., emails, SSNs, or credit card numbers) using **regex-based detection**.
   - Report violations and store them in **MongoDB Atlas** for future reference.

3. **Dashboard Visualization:**
   - Display public cloud resources and DLP violations on a **Streamlit dashboard**.
   - Real-time reporting for public buckets and sensitive data.

4. **Scalable and Secure Deployment:**
   - Uses **Docker Compose** for containerized deployment.
   - MongoDB Atlas for secure, cloud-based storage of logs and violations.

---

## Architecture
```
cloud-security-tool/
│
├── backend/
│   ├── main.py              # FastAPI backend entry point
│   ├── config.py            # Configuration (MongoDB, AWS, GCP)
│   ├── models.py            # Pydantic models for request/response
│   ├── db.py                # MongoDB Atlas connection setup
│   ├── cloud_integrations/
│   │   ├── aws.py           # AWS CloudTrail and S3 integration
│   │   ├── gcp.py           # GCP Logging and Storage integration
│
├── frontend/
│   ├── app.py               # Streamlit dashboard for results
│
├── .gitignore               # Ignore venv and other unnecessary files
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```

---

## Setup Instructions

### Prerequisites
1. **MongoDB Atlas** account.
2. **AWS** and **GCP** accounts with access keys.
3. **Docker** and **Docker Compose** installed.

### Step 1: Clone the Repository
```bash
git clone <repo-url>
cd cloud-security-tool
```

### Step 2: Configure Environment Variables
Create a `.env` file in the project root or configure your **Docker environment** with the following variables:

```
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/cloud_security?retryWrites=true&w=majority
AWS_ACCESS_KEY=<your-aws-access-key>
AWS_SECRET_KEY=<your-aws-secret-key>
GCP_CREDENTIALS=path/to/credentials.json
```

### Step 3: Start the Services
```bash
docker-compose up --build
```

### Step 4: Access the Services
- **FastAPI Backend:** http://localhost:8000/docs
- **Streamlit Dashboard:** http://localhost:8501

---

## Usage

### 1. Detect Public Buckets
- Use the `/aws/public-buckets` and `/gcp/public-buckets` endpoints to fetch public bucket information.

### 2. Report DLP Violations
- Submit a DLP violation through the API or dashboard, and it will be stored in MongoDB Atlas.

### Example Curl Request
```bash
curl -X POST "http://localhost:8000/dlp/violations" -H "Content-Type: application/json" -d '{
    "service": "AWS",
    "data": "john.doe@example.com",
    "violation_type": "Email Address",
    "timestamp": "2024-10-28T12:00:00Z"
}'
```

---

## Project Components

### Backend (FastAPI)
- **Endpoints:**
  - `/aws/public-buckets`: Get public AWS buckets.
  - `/gcp/public-buckets`: Get public GCP buckets.
  - `/dlp/violations`: Report a DLP violation.

### Frontend (Streamlit)
- **Dashboard:** Displays cloud resources and DLP violations.

### Database (MongoDB Atlas)
- **Collections:** `dlp_violations` and `public_resources`.

---

## Technologies Used
- **FastAPI**: Backend API framework.
- **Streamlit**: Frontend for dashboards.
- **MongoDB Atlas**: Cloud-based NoSQL database.
- **AWS**: CloudTrail and S3 for monitoring.
- **GCP**: Logging and Storage for monitoring.
- **Docker**: Containerization.
- **Docker Compose**: Service orchestration.

---

## Troubleshooting

### 1. MongoDB Connection Issues
- Ensure the **MongoDB URI** is correct and IP whitelisting is configured.

### 2. AWS/GCP API Errors
- Check if the access keys are valid and have the required permissions.

### 3. Docker Issues
- Ensure Docker and Docker Compose are installed and running correctly.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements
- **FastAPI** for backend development.
- **Streamlit** for the dashboard.
- **MongoDB Atlas** for providing a free-tier cloud database.
- **AWS** and **GCP** for cloud integration.

---

## Contact
For any questions or issues, please contact [Your Name] at [your-email@example.com].
"""