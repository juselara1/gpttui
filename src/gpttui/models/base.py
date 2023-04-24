"""
This module defines the general classes required to integrate different models.
"""
from abc import ABC, abstractmethod

from pydantic import BaseModel
from gpttui.database.base import AbstractDB
from enum import Enum

class ModelsEnum(Enum):
    """
    This enum defines the available models.
    """
    OPENAI = "OPENAI"
    CHATSONIC = "CHATSONIC"

class AbstractModel(ABC):
    """
    This abstract class defines any generative model.

    Attributes
    ----------
    model_name : str
        Model name.
    session_name : str
        Session name.
    context : str
        Context given to the model.
    database : AbstractDB
        Database to store the messages.
    """
    config: BaseModel
    session_name: str
    context: str
    database: AbstractDB

    def add_context(self, context: str) -> "AbstractModel":
        """
        Sets the context.

        Parameters
        ----------
        context : str
            Context given to the model.

        Returns
        -------
        AbstractModel
            Instance of the model to use as a builder.
        """
        self.context = context
        return self

    @abstractmethod
    def setup(self, config: BaseModel, session_name: str, database: AbstractDB) -> "AbstractModel":
        """
        This method is used to setup any model.

        Parameters
        ----------
        config : BaseModel
            Dataclass with the model's config options.
        session_name : str
            Session name.
        database : AbstractDB
            Database to store the messages.

        Returns
        -------
        AbstractModel
            Instance of the model to use as a builder.
        """
        ...

    @abstractmethod
    async def get_answer(self, message: str) -> str:
        """
        Generates an answer given an input message.

        Parameters
        ----------
        message : str
            Input text.

        Returns
        -------
        str
            Response.
        """
        ...
