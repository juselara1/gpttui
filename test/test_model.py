import pytest
from gpttui.database.base import AbstractDB
from gpttui.models.base import AbstractModel
from gpttui.models.openai import OpenAIModel
from gpttui.database.sqlite import SqliteDB
from typing import Tuple

class TestOpenAi:
    @staticmethod
    def setup_model() -> Tuple[AbstractDB, AbstractModel]:
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
        db, model = (
                TestOpenAi
                .setup_model()
                )
        db.create_session(session_name="test")
        answer = model.get_answer(message)
        db.delete_session(session_name="test")
        assert isinstance(answer, str)
