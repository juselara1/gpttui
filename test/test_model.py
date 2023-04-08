import pytest
from gpttui.models.base import AbstractModel
from gpttui.models.openai import OpenAIModel

class TestOpenAi:
    @staticmethod
    def setup_model() -> AbstractModel:
        model = (
                OpenAIModel()
                .add_context(context="You're an expert programmer")
                .init_model(model_name="gpt-3.5-turbo")
                )
        return model

    @pytest.mark.parametrize("message", [
        "Is Python better than JS?",
        "How to write hello word in Python?"
        ])
    def test_generation(self, message: str):
        answer = (
                TestOpenAi
                .setup_model()
                .get_answer(message)
                )
        assert isinstance(answer, str)
