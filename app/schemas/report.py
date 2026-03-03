from pydantic import BaseModel
from typing import List, Optional


class RuleResultSchema(BaseModel):
    rule: str
    status: str
    severity: str
    details: Optional[str] = None


class SummarySchema(BaseModel):
    total: int
    passed: int
    failed: int


class ReportSchema(BaseModel):
    request_id: str
    overall_status: str
    summary: SummarySchema
    results: List[RuleResultSchema]
