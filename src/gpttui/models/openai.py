import openai, os
import time
from gpttui.models.base import AbstractModel
from gpttui.database.base import Messages, Message, MessageWithTime
from typing import Any

class OpenAIModel(AbstractModel):
    model_name: str

    def auth(self):
        openai.organization = os.getenv( "OPENAI_ORG" )
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def init_model(self, **kwargs: Any) -> "OpenAIModel":
        self.model_name = kwargs["model_name"]
        return self

    def last_messages(self) -> Messages:
        msgs = [
                Message(role="system", content=self.context)
                ]
        return Messages(
                values=msgs
                )

    def get_answer(self, message: str) -> Any:
        last_msgs = self.last_messages()
        last_msgs.values.append(
                Message(role="user", content=message)
                )
        response = str(
                openai.ChatCompletion.create(
                    model = self.model_name,
                    messages = last_msgs.dict()["values"]
                    )
                .choices[0].message.content #type: ignore
                )
        return response
