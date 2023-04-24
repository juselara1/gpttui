"""
This module contains the integration with ChatSonic.
"""
import time
from typing import List
from pydantic import BaseModel
from gpttui.models.base import AbstractModel
from gpttui.database.base import Messages, Message, MessageWithTime, AbstractDB
try:
    import httpx, ssl
except ImportError:
    raise ImportError("Could not import colossal dependencies, please install it with:\n\tpip install gpttui[colossal]")

class ColossalConf(BaseModel):
    """
    Dataclass with the config for the colossal model.
    """
    url : str = "https://service.colossalai.org/generate"
    repetition_penalty: float = 1.2
    top_k : int = 40
    top_p : float = 0.5
    temperature : float = 0.7
    max_new_tokens : int = 512
    timeout: float = 30

class ColossalMessage(BaseModel):
    """
    Represents a single message.
    """
    instruction : str
    response : str

class ColossalMessages(BaseModel):
    """
    Represents the history of messages.
    """
    values : List[ColossalMessage]

class ColossalModel(AbstractModel):
    """
    This class allows loading and interacting with colossal model.
    """
    config : ColossalConf

    def setup(self, config: ColossalConf, session_name: str, database: AbstractDB) -> "ColossalModel":
        """
        Initializes the model.

        Parameters
        ----------
        config : ColossalConf
            Configuration options.
        session_name : str
            Session name.
        database : AbstractDB
            Database.

        Returns
        -------
        ColossalConf
            Instance of the model to be used as a builder.
        """
        self.config = config
        self.session_name = session_name
        self.database = database
        return self

    @staticmethod
    def parse_messages(msgs: Messages) -> ColossalMessages:
        """
        This method parses general messages into colossal specific messages.

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
        user = filter(lambda x: x.role == "user", msgs.values)
        assistant = filter(lambda x: x.role == "assistant", msgs.values)
        for umsg, amsg in zip(user, assistant):
            parsed_msgs.append(
                    ColossalMessage(instruction=umsg.content, response=amsg.content)
                    )
        return ColossalMessages(values=parsed_msgs)

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
        history = ColossalModel.parse_messages(last_msgs)
        history.values.append(ColossalMessage(instruction=message, response=""))
        payload = {
                "repetition_penalty": self.config.repetition_penalty,
                "top_k": self.config.top_k,
                "top_p": self.config.top_p,
                "temperature": self.config.temperature,
                "max_new_tokens": self.config.max_new_tokens,
                "history": history.dict()["values"]
                } 
        context = ssl._create_unverified_context()
        timeout = httpx.Timeout(self.config.timeout)
        async with httpx.AsyncClient(verify=context, timeout=timeout) as client:
            r = await client.post(self.config.url, json=payload)
            response = r.text

        new_msg = MessageWithTime(
                message=Message(role="assistant", content=response),
                timestamp=int(time.time())
                )
        self.database.add_message(msg=new_msg, session_name=self.session_name)
        return response
