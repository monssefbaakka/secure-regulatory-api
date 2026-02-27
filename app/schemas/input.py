from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from uuid import UUID
from decimal import Decimal
from typing import Dict, Any

class InputSchema(BaseModel):
    user_id: UUID
    email: EmailStr
    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
        description="Transaction amount, must be greater than 0 with up to 2 decimals"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional additional data"
    )

    model_config = ConfigDict(extra="forbid")

    @field_validator('metadata')
    def metadata_keys_must_be_str(cls, v):
        if not all(isinstance(k, str) for k in v.keys()):
            raise ValueError("All metadata keys must be strings")
        return v