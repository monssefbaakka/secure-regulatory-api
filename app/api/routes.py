from fastapi import APIRouter, Request
from app.schemas.input import InputSchema
from app.schemas.report import ReportSchema, RuleResultSchema, SummarySchema
from app.services.validation import validate_data

router = APIRouter()


@router.post("/validate", response_model=ReportSchema)
async def validate_endpoint(payload: InputSchema, request: Request):
    """
    Validate incoming payload and return a structured report.
    """
    rule_results: list[RuleResultSchema] = validate_data(payload.model_dump())

    total = len(rule_results)
    passed = sum(1 for r in rule_results if r.status.lower() == "passed")
    failed = total - passed

    summary = SummarySchema(total=total, passed=passed, failed=failed)
    overall_status = "success" if failed == 0 else "failure"

    return ReportSchema(
        request_id=getattr(request.state, "correlation_id", ""),
        overall_status=overall_status,
        summary=summary,
        results=rule_results
    )