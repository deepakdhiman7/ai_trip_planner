import os
from utils.config_loader import load_config
from pydantic import BaseModel, PrivateAttr, SecretStr
from typing import Literal, Optional, Any
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    # store loaded config as a private attribute
    _config: Optional[dict] = PrivateAttr(default=None)

    def model_post_init(self, _context: Any) -> None:
        self._config = load_config()

    def load_llm(self):
        mapper = {"groq": self._load_groq,
                  "openai": self._load_openai}
        loader_fn = mapper[self.model_provider]
        return loader_fn()

    def _load_groq(self):
        print("Loading LLM from Groq..............")
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key is None:
            raise ValueError("GROQ_API_KEY not set in environment")
        # ensure config is loaded
        if self._config is None:
            raise ValueError("Config not loaded")
        model_name = self._config["llm"]["groq"]["model"]
        llm = ChatGroq(model=model_name, api_key=SecretStr(groq_api_key))
        return llm

    def _load_openai(self):
        print("Loading LLM from OpenAI..............")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key is None:
            raise ValueError("OPENAI_API_KEY not set in environment")
        # ensure config is loaded
        if self._config is None:
            raise ValueError("Config not loaded")
        model_name = self._config["llm"]["openai"]["model"]
        llm = ChatOpenAI(model=model_name, api_key=SecretStr(openai_api_key))
        return llm