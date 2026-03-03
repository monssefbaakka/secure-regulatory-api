from app.rules.business_rules import (
    AmountMaxLimitRule,
    EmailDomainRule,
    UserIdUUIDRule,
    NoEmptyStringsRule,
)
from app.rules.security_rules import (
    NoScriptInjectionRule,
    NoSuspiciousKeysRule,
)


def test_amount_max_limit_pass():
    rule = AmountMaxLimitRule()

    payload = {"amount": 5000}
    result = rule.evaluate(payload)

    assert result.status == "passed"


def test_amount_max_limit_fail():
    rule = AmountMaxLimitRule()

    payload = {"amount": 20000}
    result = rule.evaluate(payload)

    assert result.status == "failed"


def test_email_domain_allowed():
    rule = EmailDomainRule()

    payload = {"email": "user@company.com"}
    result = rule.evaluate(payload)

    assert result.status == "passed"


def test_email_domain_blocked():
    rule = EmailDomainRule()

    payload = {"email": "user@gmail.com"}
    result = rule.evaluate(payload)

    assert result.status == "failed"


def test_valid_uuid():
    rule = UserIdUUIDRule()

    payload = {"user_id": "550e8400-e29b-41d4-a716-446655440000"}
    result = rule.evaluate(payload)

    assert result.status == "passed"


def test_invalid_uuid():
    rule = UserIdUUIDRule()

    payload = {"user_id": "invalid-uuid"}
    result = rule.evaluate(payload)

    assert result.status == "failed"


def test_empty_string_detected():
    rule = NoEmptyStringsRule()

    payload = {"name": ""}
    result = rule.evaluate(payload)

    assert result.status == "failed"


def test_suspicious_key_detected():
    rule = NoSuspiciousKeysRule()

    payload = {"password": "123"}
    result = rule.evaluate(payload)

    assert result.status == "failed"


def test_script_injection_detected():
    rule = NoScriptInjectionRule()

    payload = {"comment": "<script>alert('xss')</script>"}

    result = rule.evaluate(payload)

    assert result.status == "failed"
    assert result.severity == "critical"


def test_script_injection_nested():
    rule = NoScriptInjectionRule()

    payload = {"user": {"bio": "Hello <script>malicious()</script>"}}

    result = rule.evaluate(payload)

    assert result.status == "failed"


def test_script_injection_not_present():
    rule = NoScriptInjectionRule()

    payload = {"comment": "Hello world"}

    result = rule.evaluate(payload)

    assert result.status == "passed"
