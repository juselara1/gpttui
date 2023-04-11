"""
Defines the tests that are performed over models.
"""
import pytest
from gpttui.database.base import AbstractDB
from gpttui.models.base import AbstractModel
from gpttui.models.openai import OpenAIModel
from gpttui.database.sqlite import SqliteDB
from typing import Tuple

class TestOpenAi:
    """
    Tests that are used for any OpenAI model.
    """
    @staticmethod
    def setup_model() -> Tuple[AbstractDB, AbstractModel]:
        """
        Initialize the model and the database.

        Returns
        -------
        Tuple[AbstractDB, AbstractModel]
            Initialized database and model.
        """
        db = (
                SqliteDB()
                .setup(database="test.db")
                )
        model = (
                OpenAIModel()
                .add_context(context="You're an expert programmer")
                .setup(model_name="gpt-3.5-turbo", database=db, session_name="test")
                )
        return db, model

    @pytest.mark.parametrize("message", [
        "Is Python better than JS?",
        "How to write hello word in Python?"
        ])
    def test_generation(self, message: str):
        """
        Tests the generation from the models.

        Parameters
        ----------
        message : str
            Input message.
        """
        db, model = (
                TestOpenAi
                .setup_model()
                )
        db.create_session(session_name="test")
        answer = model.get_answer(message)
        db.delete_session(session_name="test")
        assert isinstance(answer, str)
