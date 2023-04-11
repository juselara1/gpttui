"""
This module defines the general classes that are required in the database module.
"""

from abc import ABC, abstractmethod
from typing import List, Any
from pydantic import BaseModel
from enum import Enum

class DatabasesEnum(Enum):
    """
    Enum that specifies the supported databases.
    """
    SQLITE = "SQLITE"

class Message(BaseModel):
    """
    Dataclass that contains a single message.

    Attributes
    ----------
    role : str
        Who wrote the message.
    content : str
        Message content.
    """
    role: str
    content: str

class Messages(BaseModel):
    """
    Dataclass that represents multiple messages.

    Attributes
    ----------
    values : List[Message]
        List of messages.
    """
    values: List[Message]

class MessageWithTime(BaseModel):
    """
    Dataclass that represents a message and its timestamp.

    Attributes
    ----------
    message : Message
        A message instance.
    timestamp : int
        Unix time.
    """
    message: Message
    timestamp: int

class AbstractDB(ABC):
    """
    Abstract class that represents any compatible database.

    Attributes
    ----------
    connection : Any
        Connection with any database.
    """
    connection: Any

    @abstractmethod
    def setup(self, **kwargs: str) -> "AbstractDB":
        """
        This method must be used to setup the database. For instance, to add connection strings, clients, among others.

        Parameters
        ----------
        kwargs : str
            Any string keyword argument.

        Returns
        -------
        AbstractDB
            Instance of the database to use the method as a builder.
        """
        ...

    @abstractmethod
    def create_session(self, session_name: str):
        """
        This method is intended to create a session.

        Parameters
        ----------
        session_name : str
            Name of the session.
        """
        ...

    @abstractmethod
    def delete_session(self, session_name: str):
        """
        This method is intended to delete a session.

        Parameters
        ----------
        session_name : str
            Name of the session.
        """
        ...

    @abstractmethod
    def add_message(self, msg: MessageWithTime, session_name: str):
        """
        Add a message to the database.

        Parameters
        ----------
        msg : MessageWithTime
            Message to store.
        session_name : str
            Name of the session.
        """
        ...

    @abstractmethod
    def get_messages(self, session_name: str) -> Messages:
        """
        Get the most recent messages from the database.

        Parameters
        ----------
        session_name : str
            Name of the session.
        """
        ...

    @abstractmethod
    def close(self):
        """
        This method allows closing the connection.
        """
        ...
