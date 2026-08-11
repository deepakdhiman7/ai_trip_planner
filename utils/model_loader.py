from utils.config_loader import load_config
from pydantic import BaseModel, Field
from typing import Literal, Optional

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[dict] = Field(default=None, exclude=True)


