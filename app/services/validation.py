from typing import Dict, Any, List
from app.schemas.report import RuleResultSchema
from app.rules.engine import RulesEngine, run_rules
from app.core.security import run_security_checks


def validate_data(payload: Dict[str, Any]) -> List[RuleResultSchema]:
    """Orchestrates rules engine and cross-field checks."""
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
                rule="high_priority_min_amount", status="passed", severity="medium"
            )
        )

    return results


def validate_data(payload: dict) -> list[RuleResultSchema]:
    security_error = run_security_checks(payload)
    if security_error:
        return [
            RuleResultSchema(
                rule="security_precheck",
                status="failed",
                severity="critical",
                details=security_error,
            )
        ]

    return run_rules(payload)
