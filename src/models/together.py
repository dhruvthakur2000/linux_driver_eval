#from openai import OpenAI
import os
from together import Together
from src.logger import logger
from src.errors import ModelLoadError, CodeGenerationError

class TogetherModel:
    def __init__(self, model_name: str, api_key: str):
        if not api_key:
            raise ValueError("TOGETHER_API_KEY not found in environment")

        self.model_name = model_name
        self.client = Together(api_key=api_key)
        logger.info(f"TogetherModel initialized with model: {model_name}")


    def generate_code(self, prompt: str, max_tokens: int = 1024) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You need assess how well AI coding models perform at writing Linux device drivers"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=max_tokens
            )
            generated = response.choices[0].message.content
            logger.info(" Code generation successful from Together API")
            return generated
        except Exception as e:
            logger.error(f" Together AI generation failed inside generate_code(): {e}")
            # Don't mention `response` at all here
            raise CodeGenerationError(f"Together API Error: {e}")


        


"""class TogetherModel:
    def __init__(self, model_name: str,api_key):
        self.model_name = model_name
        api_key = os.getenv("TOGETHER_API_KEY")

        if not api_key:
            raise ValueError("TOGETHER_API_KEY not found in environment")

        logger.info(f"🔗 TogetherModel initialized with model: {model_name}")

        self.client = OpenAI(
            base_url="https://api.together.xyz/v1",
            api_key=api_key  # ✅ MAKE SURE THIS LINE EXISTS
        ) 
"""

