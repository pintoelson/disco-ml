from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

class GitHubComment(BaseModel):
    id: str
    author: str
    timestamp: datetime
    body: str
    classification: Optional[str] = None  # Pro, Con, Neutral, NA, etc.
    justification: Optional[str] = None # Why LLM classified it this way

class GitHubItem(BaseModel):
    id: str
    item_type: str  # "issue", "pr", "discussion"
    number: int
    title: str
    body: str
    author: str
    timestamp: datetime
    status: str
    comments: List[GitHubComment] = []
    lifecycle_stage: Optional[str] = None
    lifecycle_artifact: Optional[str] = None
    lifecycle_justification: Optional[str] = None
    
class VersionedItem(BaseModel):
    version_id: str  # e.g., "{item_id}_v_{timestamp}"
    parent_id: str
    parent_type: str
    parent_number: int
    author: str
    timestamp: datetime
    status: str
    text_content: str  # The accumulated text context
    trigger_classification: str # Pro, Con, Neutral
    lifecycle_stage: Optional[str] = None
    lifecycle_artifact: Optional[str] = None
    lifecycle_justification: Optional[str] = None
    
class DecisionFormalization(BaseModel):
    version_id: str
    filename: Optional[str] = None
    author: Optional[str] = None
    timestamp: Optional[datetime] = None
    status: Optional[str] = None
    lifecycle_stage: Optional[str] = None
    lifecycle_artifact: Optional[str] = None
    schema_data: Dict[str, Any]
