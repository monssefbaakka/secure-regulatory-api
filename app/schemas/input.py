from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any

class DynamicInputSchema(BaseModel):
    payload: Dict[str, Any] = Field(..., description="Arbitrary JSON payload")

    model_config = {
        "extra": "forbid",
        "strict": True
    }

    @field_validator("payload")
    def prevent_empty_payload(cls, v):
        if not v:
            raise ValueError("Payload cannot be empty")
        return v