"""
This module contains the integration with OpenAI models.
"""
import openai, os, time
from openai.error import Timeout
from gpttui.models.base import AbstractModel
from gpttui.database.base import Messages, Message, MessageWithTime
from typing import Any

class OpenAIModel(AbstractModel):
    """
    This class allows loading and interacting with any openai model through its API.
    """
    timeout = 0
    max_retries = 3

    def setup(self, **kwargs: Any) -> "OpenAIModel":
        """
        Initializes the model and collects credentials for OpenAI.

        Parameters
        ----------
        model_name : str
            Model name.
        session_name : str
            Session name.
        database : AbstractDB
            Database to store the messages.

        Returns
        -------
        OpenAIModel
            Instance of the model to be used as a builder.
        """
        self.model_name = kwargs["model_name"]
        self.session_name = kwargs["session_name"]
        self.database = kwargs["database"]
        openai.organization = os.getenv("OPENAI_ORG")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        return self

    def last_messages(self) -> Messages:
        """
        Extracts the most recent messages from the database.

        Returns
        -------
        Messages
            Most recent messages.
        """
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

    async def get_answer(self, message: str) -> str:
        """
        Obtains an answer form any message.

        Parameters
        ----------
        message : str
            Input message.

        Returns
        -------
        str
            Generated response.
        """
        last_msgs = self.last_messages()
        new_msg = MessageWithTime(
                message=Message(role="user", content=message),
                timestamp=int(time.time())
                )
        self.database.add_message(msg=new_msg, session_name=self.session_name)
        last_msgs = self.last_messages()
        response = ""
        retries = 0
        while not response and retries < self.max_retries:
            try:
                response = await openai.ChatCompletion.acreate(
                            model = self.model_name,
                            messages = last_msgs.dict()["values"],
                            request_timeout = self.timeout
                            )
            except Timeout:
                retries += 1
        response = str(response.choices[0].message.content) # type: ignore
        if retries == 3:
            raise Timeout("Maximum number of retries achieved.")
        new_msg = MessageWithTime(
                message=Message(role="assistant", content=response),
                timestamp=int(time.time())
                )
        self.database.add_message(msg=new_msg, session_name=self.session_name)
        return response
