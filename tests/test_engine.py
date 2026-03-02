from app.rules.engine import RulesEngine

def test_engine_all_pass():
    engine = RulesEngine()

    payload = {
        "amount": 5000,
        "email": "user@company.com",
        "user_id": "550e8400-e29b-41d4-a716-446655440000"
    }

    results = engine.run(payload)

    assert all(r.status == "passed" for r in results)
    
def test_engine_amount_failure():
    engine = RulesEngine()

    payload = {
        "amount": 20000
    }

    results = engine.run(payload)

    assert any(r.rule == "amount_max_limit" and r.status == "failed"
               for r in results)

def test_engine_suspicious_key():
    engine = RulesEngine()

    payload = {
        "password": "123456"
    }

    results = engine.run(payload)

    assert any(r.rule == "no_suspicious_keys" and r.status == "failed"
               for r in results)
    
def test_engine_multiple_failures():
    engine = RulesEngine()

    payload = {
        "password": "123",
        "amount": 20000,
        "name": ""
    }

    results = engine.run(payload)

    failed = [r for r in results if r.status == "failed"]

    assert len(failed) >= 2
    
def test_engine_rule_count():
    engine = RulesEngine()

    assert len(engine.rules) == 6