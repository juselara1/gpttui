from abc import ABC, abstractmethod
from typing import List, Any
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class Messages(BaseModel):
    values: List[Message]

class MessageWithTime(BaseModel):
    message: Message
    timestamp: int

class AbstractDB(ABC):
    connection: Any

    @abstractmethod
    def setup(self, **kwargs: str) -> "AbstractDB":
        ...

    @abstractmethod
    def create_session(self, session_name: str):
        ...

    @abstractmethod
    def delete_session(self, session_name: str):
        ...

    @abstractmethod
    def add_message(self, msg: MessageWithTime, session_name: str):
        ...

    @abstractmethod
    def get_messages(self, session_name: str) -> Messages:
        ...

    @abstractmethod
    def close(self):
        ...
