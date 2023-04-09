from abc import ABC, abstractmethod
from gpttui.database.base import AbstractDB
from typing import Any

class AbstractModel(ABC):
    endpoint: str
    context: str
    database: AbstractDB

    def add_context(self, context: str) -> "AbstractModel":
        self.context = context
        return self

    @abstractmethod
    def setup(self, *args: Any, **kwargs: Any) -> "AbstractModel":
        ...

    @abstractmethod
    def init_model(self, **kwargs: Any) -> "AbstractModel":
        ...

    @abstractmethod
    def get_answer(self, message: str) -> str:
        ...
