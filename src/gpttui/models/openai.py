"""
This module contains the integration with OpenAI models.
"""
try:
    import openai, time
    from openai.error import Timeout
except ImportError:
    raise ImportError("Could not import openai library, please install it with:\n\tpip install gpttui[openai]")
from pydantic import BaseModel
from gpttui.models.base import AbstractModel
from gpttui.database.base import AbstractDB, Message, MessageWithTime

class OpenAIConf(BaseModel):
    """
    Dataclass to setup OpenAI models.
    """
    timeout : int = 30
    max_retries : int = 3
    model_name : str = "gpt-3.5-turbo"
    organization : str = ""
    api_key : str = ""

class OpenAIModel(AbstractModel):
    """
    This class allows loading and interacting with any openai model through its API.
    """
    config : OpenAIConf

    def setup(self, config: OpenAIConf, session_name: str, database: AbstractDB) -> "OpenAIModel":
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
        self.config = config
        self.session_name = session_name
        self.database = database
        openai.organization = config.organization
        openai.api_key = config.api_key
        return self

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
        while not response and retries < self.config.max_retries:
            try:
                response = await openai.ChatCompletion.acreate(
                            model = self.config.model_name,
                            messages = last_msgs.dict()["values"],
                            request_timeout = self.config.timeout
                            )
            except Timeout:
                retries += 1
        if retries == self.config.max_retries:
            raise Timeout("Maximum number of retries achieved.")
        response = str(response.choices[0].message.content) # type: ignore
        new_msg = MessageWithTime(
                message=Message(role="assistant", content=response),
                timestamp=int(time.time())
                )
        self.database.add_message(msg=new_msg, session_name=self.session_name)
        return response
