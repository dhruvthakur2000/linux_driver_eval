from transformers import AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline
from .base import BaseModel


class DeepSeekModel(BaseModel):
    def __init__(self, model_id="deepseek-ai/deepseek-coder-1.3b-base"):
        pass