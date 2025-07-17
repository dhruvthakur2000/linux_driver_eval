from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from src.errors import ModelLoadError

class PhiModel:
    def __init__(self, model_id="microsoft/phi-2"):
        self.model_id = model_id
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")
            self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        except Exception as e:
            raise ModelLoadError(f"Failed to load Phi model: {str(e)}")

    def generate_code(self, prompt: str) -> str:
        output = self.generator(prompt, max_new_tokens=300, do_sample=True)[0]["generated_text"]
        return output.replace(prompt, "").strip()