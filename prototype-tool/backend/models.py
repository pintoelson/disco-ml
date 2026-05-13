from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum

class MLLifecycleActivity(str, Enum):
    Business_and_Data_Understanding = "Business_and_Data_Understanding"
    Data_Engineering = "Data_Engineering"
    Model_Engineering = "Model_Engineering"
    Model_Evaluation = "Model_Evaluation"
    ModelDeployment = "ModelDeployment"
    ModelMonitoring = "ModelMonitoring"
    MLLifecycleActivity = "MLLifecycleActivity" # Fallback

class MLRole(str, Enum):
    DataEngineer = "DataEngineer"
    MLEngineer = "MLEngineer"
    DataScientist = "DataScientist"
    SoftwareEngineer = "SoftwareEngineer"
    ITOpsTeam = "ITOpsTeam"
    ProjectTeam = "ProjectTeam"
    Role = "Role" # Fallback

class MLAssetClass(str, Enum):
    Dataset = "Dataset"
    MLAsset = "MLAsset"
    FeatureSet = "FeatureSet"
    ProvenanceRecord = "ProvenanceRecord"

class ArgumentInput(BaseModel):
    author: str
    timestamp: str
    classification: str
    argument: str

class AssetInput(BaseModel):
    name: str
    asset_type: MLAssetClass
    location: Optional[str] = None

class IssueInput(BaseModel):
    title: str
    body: str
    author: str
    timestamp: str

class DecisionInput(BaseModel):
    decision: Optional[str] = None
    authors: List[str] = []

class DecisionTicket(BaseModel):
    filename: Optional[str] = None
    status: str
    timestamp: str
    Issue: Union[str, IssueInput]
    Decision: Optional[DecisionInput] = None
    Rationale: Optional[str] = None
    Cost: Optional[str] = None
    Risk: Optional[str] = None
    Argument: Optional[List[ArgumentInput]] = None

class MLElements(BaseModel):
    lifecycle_stage: Optional[MLLifecycleActivity] = None
    main_assets: Optional[List[AssetInput]] = None
    mentioned_assets: Optional[List[AssetInput]] = None
    author_roles: Optional[Dict[str, MLRole]] = None

class IngestionPayload(BaseModel):
    decision_ticket: DecisionTicket
    ml_elements: Optional[MLElements] = None
