from fastapi import APIRouter, Depends, Request
from uuid import uuid4
import logging

from app.core.security import validate_api_key, precheck_payload_structure, mask_sensitive_data
from app.rules.engine import RulesEngine
from app.schemas.report import ReportSchema, SummarySchema, RuleResultSchema
from app.schemas.input import DynamicInputSchema

router = APIRouter()
engine = RulesEngine()
logger = logging.getLogger(__name__)


@router.post(
    "/validate",
    response_model=ReportSchema,
    dependencies=[Depends(validate_api_key)]
)
async def validate_endpoint(payload_schema: DynamicInputSchema, request: Request):

    request_id = str(uuid4())
    payload = payload_schema.payload

    security_error = precheck_payload_structure(payload)
    if security_error:
        logger.warning(
            "Security precheck failed",
            extra={"request_id": request_id}
        )

        return ReportSchema(
            request_id=request_id,
            overall_status="failure",
            summary=SummarySchema(total=1, passed=0, failed=1),
            results=[
                RuleResultSchema(
                    rule="security_precheck",
                    status="failed",
                    severity="critical",
                    details=security_error
                )
            ]
        )

    results = engine.run(payload)

    passed = sum(1 for r in results if r.status == "passed")
    failed = sum(1 for r in results if r.status == "failed")
    overall_status = "success" if failed == 0 else "failure"

    safe_payload = mask_sensitive_data(payload, fields_to_mask=["password", "token", "secret"])

    logger.info(
        "Validation executed",
        extra={
            "request_id": request_id,
            "failed_rules": failed,
            "payload_preview": str(safe_payload)[:200]
        }
    )

    return ReportSchema(
        request_id=request_id,
        overall_status=overall_status,
        summary=SummarySchema(total=len(results), passed=passed, failed=failed),
        results=results
    )