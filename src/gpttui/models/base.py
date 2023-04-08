from abc import ABC, abstractmethod
from typing import Any

class AbstractModel(ABC):
    endpoint: str
    context: str
    database: str

    #TODO: implement database.

    def add_endpoint(self, endpoint: str) -> "AbstractModel":
        self.endpoint = endpoint
        return self

    def add_context(self, context: str) -> "AbstractModel":
        self.context = context
        return self

    @abstractmethod
    def init_model(self, **kwargs: Any) -> "AbstractModel":
        ...

    @abstractmethod
    def get_answer(self, message: str) -> str:
        ...
