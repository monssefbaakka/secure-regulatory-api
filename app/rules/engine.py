from typing import List, Dict, Any
from app.schemas.report import RuleResultSchema
from app.rules.base import BaseRule

from app.rules.business_rules import (
    AmountMaxLimitRule,
    EmailDomainRule,
    NoEmptyStringsRule,
    UserIdUUIDRule,
)
from app.rules.security_rules import (
    NoSuspiciousKeysRule,
    NoScriptInjectionRule,
)


class RulesEngine:
    def __init__(self, rules: List[BaseRule] | None = None):
        self.rules = rules or [
            AmountMaxLimitRule(),
            EmailDomainRule(),
            NoEmptyStringsRule(),
            UserIdUUIDRule(),
            NoSuspiciousKeysRule(),
            NoScriptInjectionRule(),
        ]

    def run(self, payload: Dict[str, Any]) -> List[RuleResultSchema]:
        return [rule.evaluate(payload) for rule in self.rules]
