import pytest
from pydantic import ValidationError
from app.schemas.input import DynamicInputSchema

def test_valid_payload():
    payload = {
        "payload": {
            "user": {"id": "550e8400-e29b-41d4-a716-446655440000"},
            "transaction": {"amount": 7500}
        }
    }
    schema = DynamicInputSchema(**payload)
    assert schema.payload["user"]["id"] == "550e8400-e29b-41d4-a716-446655440000"

def test_missing_payload_key():
    payload = {"user": {"id": "550e8400-e29b-41d4-a716-446655440000"}}
    with pytest.raises(ValidationError) as exc:
        DynamicInputSchema(**payload)
    assert "Field required" in str(exc.value)

def test_extra_field_not_allowed():
    payload = {"payload": {"amount": 500}, "extra_field": "not allowed"}
    with pytest.raises(ValidationError) as exc:
        DynamicInputSchema(**payload)
    assert "Extra inputs are not permitted" in str(exc.value)

def test_nested_complex_json():
    payload = {
        "payload": {
            "level1": {
                "level2": {"level3": {"amount": 100, "note": "deeply nested"}}
            },
            "list_field": [{"id": 1}, {"id": 2}]
        }
    }
    schema = DynamicInputSchema(**payload)
    assert schema.payload["level1"]["level2"]["level3"]["amount"] == 100
    assert len(schema.payload["list_field"]) == 2

def test_invalid_type():
    payload = {"payload": "this should be a dict"}
    with pytest.raises(ValidationError) as exc:
        DynamicInputSchema(**payload)
    assert "Input should be a valid dictionary" in str(exc.value)