from app.schemas.report import ReportSchema, SummarySchema, RuleResultSchema
from typing import List


class ReportBuilder:

    @staticmethod
    def build_report(
        rule_results: List[RuleResultSchema], request_id: str
    ) -> ReportSchema:
        total = len(rule_results)
        passed = sum(1 for r in rule_results if r.status.lower() == "passed")
        failed = total - passed

        summary = SummarySchema(total=total, passed=passed, failed=failed)

        overall_status = "success" if failed == 0 else "failure"

        return ReportSchema(
            request_id=request_id,
            overall_status=overall_status,
            summary=summary,
            results=rule_results,
        )
