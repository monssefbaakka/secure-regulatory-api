from typing import Dict, Any, List
from app.schemas.report import RuleResultSchema
from app.rules.engine import RulesEngine
from app.core.security import precheck_payload_structure


def validate_data(payload: Dict[str, Any]) -> List[RuleResultSchema]:
    """Main validation orchestrator."""

    security_error = precheck_payload_structure(payload)
    if security_error:
        return [
            RuleResultSchema(
                rule="security_precheck",
                status="failed",
                severity="critical",
                details=security_error,
            )
        ]

    engine = RulesEngine()
    results = engine.run(payload)

    metadata = payload.get("metadata", {})
    amount = payload.get("amount", 0)

    if metadata.get("priority") == 5 and amount < 500:
        results.append(
            RuleResultSchema(
                rule="high_priority_min_amount",
                status="failed",
                severity="medium",
                details="High priority requests must have at least 500 amount",
            )
        )
    else:
        results.append(
            RuleResultSchema(
                rule="high_priority_min_amount",
                status="passed",
                severity="medium",
            )
        )

    return results