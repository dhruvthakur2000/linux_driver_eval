from transformers import AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline
from .base import BaseModel


class StarCoderModel(BaseModel):
    def __init__(self, model_id="mistralai/Mistral-7B-Instruct-v0.1"):
        pass