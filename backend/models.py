from pydantic import BaseModel

class PublicResource(BaseModel):
    service: str
    resource_name: str
    visibility: str
    timestamp: str

class DLPViolation(BaseModel):
    service: str
    data: str
    violation_type: str
    timestamp: str