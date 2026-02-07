from datetime import datetime

from pydantic import BaseModel


class LeadCreate(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    source: str | None = None


class LeadRead(LeadCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PipelineStageCreate(BaseModel):
    name: str
    order_index: int = 0


class PipelineStageRead(PipelineStageCreate):
    id: int

    class Config:
        from_attributes = True


class DealCreate(BaseModel):
    title: str
    value: int = 0
    lead_id: int
    stage_id: int


class DealRead(DealCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityCreate(BaseModel):
    lead_id: int
    note: str


class ActivityRead(ActivityCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AgentStateRead(BaseModel):
    id: int
    status: str
    last_reason: str | None = None
    updated_at: datetime

    class Config:
        from_attributes = True


class AgentStateUpdate(BaseModel):
    status: str
    last_reason: str | None = None


class AgentScriptCreate(BaseModel):
    name: str
    description: str | None = None
    content: str


class AgentScriptRead(AgentScriptCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
