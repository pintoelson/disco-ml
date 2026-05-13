from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

class GitHubComment(BaseModel):
    id: str
    author: str
    timestamp: datetime
    body: str

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
    
class VersionedItem(BaseModel):
    version_id: str  # e.g., "{item_id}_v_{timestamp}"
    parent_id: str
    parent_type: str
    parent_number: int
    author: str
    timestamp: datetime
    status: str
    text_content: str  # The trigger text (body for v1, comment for v2+)
    previous_version_id: Optional[str] = None # For incremental formalization
    
class DecisionFormalization(BaseModel):
    decision_ticket: Dict[str, Any] = {}

class MLAsset(BaseModel):
    name: str = Field(..., description="Name of the ML asset")
    asset_type: str = Field(..., description="Type of asset (Dataset, Model, Code, Feature Set, Provenance, or NA)")
    location: Optional[str] = Field(None, description="Link or location of the asset")
    discussed_by: List[str] = Field(default_factory=list, description="List of authors who discussed this asset")
    current_state: Optional[str] = Field(None, description="Current state of the asset (e.g., 'Proposed', 'In Development', 'Implemented')")

class MLElements(BaseModel):
    lifecycle_stage: str = Field(..., description="The MLOps lifecycle stage")
    main_assets: List[MLAsset] = Field(default_factory=list, description="Primary assets discussed")
    mentioned_assets: List[MLAsset] = Field(default_factory=list, description="Assets mentioned in passing")
    author_roles: Dict[str, str] = Field(default_factory=dict, description="Map of GitHub username to their identified role")

class BridgedDecision(DecisionFormalization):
    ml_elements: MLElements
