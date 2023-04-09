import openai, os, time
from gpttui.models.base import AbstractModel
from gpttui.database.base import Messages, Message, MessageWithTime
from typing import Any

class OpenAIModel(AbstractModel):
    model_name: str

    def setup(self, **kwargs: Any) -> "OpenAIModel":
        self.model_name = kwargs["model_name"]
        self.session_name = kwargs["session_name"]
        self.database = kwargs["database"]
        openai.organization = os.getenv( "OPENAI_ORG" )
        openai.api_key = os.getenv("OPENAI_API_KEY")
        return self

    def last_messages(self) -> Messages:
        self.database.create_session(session_name=self.session_name)
        last_msgs = self.database.get_messages(session_name=self.session_name)
        if not len(last_msgs.values):
            msg = MessageWithTime(
                    message=Message(role="system", content=self.context),
                    timestamp=int(time.time())
                    )
            self.database.add_message(msg=msg, session_name=self.session_name)
            return self.last_messages()
        return last_msgs

    def get_answer(self, message: str) -> Any:
        new_msg = MessageWithTime(
                message=Message(role="user", content=message),
                timestamp=int(time.time())
                )
        self.database.add_message(msg=new_msg, session_name=self.session_name)
        last_msgs = self.last_messages()
        response = str(
                openai.ChatCompletion.create(
                    model = self.model_name,
                    messages = last_msgs.dict()["values"]
                    )
                .choices[0].message.content #type: ignore
                )
        return response
