from transformers import AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline
from .base import BaseModel


class CodeGemmaModel(BaseModel):
    def __init__(self, model_id="google/codegemma-2b"):
        pass