from abc import ABC, abstractmethod
from typing import Any
from app.schemas.report import RuleResultSchema


class BaseRule(ABC):
    name: str = "BaseRule"

    @abstractmethod
    def evaluate(self, payload: Any) -> RuleResultSchema:
        pass
