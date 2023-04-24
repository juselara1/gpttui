"""
This module contains the integration with ChatSonic.
"""
import time
from typing import List
from pydantic import BaseModel
from gpttui.models.base import AbstractModel
from gpttui.database.base import Messages, Message, MessageWithTime, AbstractDB
try:
    import httpx
except ImportError:
    raise ImportError("Could not import chatsonic dependencies, please install it with:\n\tpip install gpttui[chatsonic]")

class ChatSonicConf(BaseModel):
    url : str = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"
    api_key : str = ""
    enable_memory: bool = True
    enable_google_results: bool = True

class ChatSonicMessage(BaseModel):
    is_sent : bool
    message : str

class ChatSonicMessages(BaseModel):
    values : List[ChatSonicMessage]

class ChatSonicModel(AbstractModel):
    """
    This class allows loading and interacting with any openai model through its API.
    """
    config : ChatSonicConf

    def setup(self, config: ChatSonicConf, session_name: str, database: AbstractDB) -> "ChatSonicModel":
        """
        Initializes the model and collects credentials for OpenAI.

        Parameters
        ----------
        url : str
            Chatsonic URL.

        Returns
        -------
        OpenAIModel
            Instance of the model to be used as a builder.
        """
        self.config = config
        self.session_name = session_name
        self.database = database
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

    @staticmethod
    def parse_messages(msgs: Messages) -> ChatSonicMessages:
        """
        This method parses general messages into chatsonic specific messages.

        Parameters
        ----------
        msgs : Messages
            Input messages.

        Returns
        -------
        ChatSonicMessages
            Parsed messages.
        """ 
        parsed_msgs = []
        for msg in msgs.values:
            if msg.role not in ["assistant", "user"]:
                continue
            is_sent = msg.role == "user"
            parsed_msgs.append(
                    ChatSonicMessage(is_sent=is_sent, message=msg.content)
                    )
        return ChatSonicMessages(values=parsed_msgs)

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
        payload = {
                "enable_memory": self.config.enable_memory,
                "enable_google_results": self.config.enable_google_results,
                "input_text": self.context,
                "history_data": ChatSonicModel.parse_messages(last_msgs).dict()["values"]
                } 
        headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "X-API-KEY": self.config.api_key
                }
        async with httpx.AsyncClient() as client:
            r = await client.post(self.config.url, json=payload, headers=headers)
            response = r.json()["message"]

        new_msg = MessageWithTime(
                message=Message(role="assistant", content=response),
                timestamp=int(time.time())
                )
        self.database.add_message(msg=new_msg, session_name=self.session_name)
        return response
