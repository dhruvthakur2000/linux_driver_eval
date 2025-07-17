from transformers import AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline
from .base import BaseModel


class MistralModel(BaseModel):
    def __init__(self, model_id="mistralai/Mistral-7B-Instruct-v0.1", quantized=True):
        self.tokenizer=AutoTokenizer.from_pretrained(model_id)
        self.model=AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            load_in_4bit=quantized
        )
        self.pipeline = TextGenerationPipeline(model=self.model,tokenizer=self.tokenizer)


    def generate_code(self, prompt:str)->str:
        result=self.pipeline(prompt, max_new_token=500,do_sample=True)[0]['generated_text']
        return result

