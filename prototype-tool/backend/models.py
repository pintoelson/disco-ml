from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ArgumentInput(BaseModel):
    author: str
    timestamp: str
    classification: str
    argument: str

class DecisionTicketInput(BaseModel):
    version_id: str
    filename: Optional[str] = None
    author: str
    timestamp: str
    status: str
    lifecycle_stage: Optional[str] = None
    lifecycle_artifact: Optional[str] = None
    schema_data: Dict[str, Any]
