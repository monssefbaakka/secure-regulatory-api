from typing import Any, Dict
from uuid import UUID
from app.rules.base import BaseRule
from app.schemas.report import RuleResultSchema


class NoEmptyStringsRule(BaseRule):
    name = "no_empty_strings"

    def evaluate(self, payload: Dict[str, Any]) -> RuleResultSchema:
        empty_found = False

        def scan(obj: Any):
            nonlocal empty_found

            if isinstance(obj, dict):
                for value in obj.values():
                    scan(value)

            elif isinstance(obj, list):
                for item in obj:
                    scan(item)

            elif isinstance(obj, str) and obj.strip() == "":
                empty_found = True

        scan(payload)

        if empty_found:
            return RuleResultSchema(
                rule=self.name,
                status="failed",
                severity="medium",
                details="Empty string detected",
            )

        return RuleResultSchema(rule=self.name, status="passed", severity="low")


class AmountMaxLimitRule(BaseRule):
    """
    Ensures amount does not exceed business threshold.
    """

    name = "amount_max_limit"
    MAX_AMOUNT = 10000  # Matches your test expectation

    def evaluate(self, payload: Dict[str, Any]) -> RuleResultSchema:
        amount = payload.get("amount")

        if isinstance(amount, (int, float)) and amount > self.MAX_AMOUNT:
            return RuleResultSchema(
                rule=self.name,
                status="failed",
                severity="high",
                details=f"Amount exceeds maximum allowed ({self.MAX_AMOUNT})",
            )

        return RuleResultSchema(rule=self.name, status="passed", severity="low")


class EmailDomainRule(BaseRule):
    """
    Allows only specific business email domains.
    """

    name = "email_domain_allowed"
    ALLOWED_DOMAINS = {"company.com"}

    def evaluate(self, payload: Dict[str, Any]) -> RuleResultSchema:
        email = payload.get("email")

        if isinstance(email, str) and "@" in email:
            domain = email.split("@")[-1].lower()

            if domain not in self.ALLOWED_DOMAINS:
                return RuleResultSchema(
                    rule=self.name,
                    status="failed",
                    severity="medium",
                    details=f"Email domain '{domain}' not allowed",
                )

        return RuleResultSchema(rule=self.name, status="passed", severity="low")


class UserIdUUIDRule(BaseRule):
    """
    Ensures user_id is a valid UUID.
    """

    name = "user_id_must_be_uuid"

    def evaluate(self, payload: Dict[str, Any]) -> RuleResultSchema:
        user_id = payload.get("user_id")

        if user_id is None:
            return RuleResultSchema(rule=self.name, status="passed", severity="low")

        try:
            UUID(str(user_id))
        except (ValueError, TypeError):
            return RuleResultSchema(
                rule=self.name,
                status="failed",
                severity="high",
                details="user_id must be a valid UUID",
            )

        return RuleResultSchema(rule=self.name, status="passed", severity="low")
