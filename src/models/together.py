from together import Together
from src.logger import logger

class TogetherModel:
    def __init__(self, model_name: str):
        self.client = Together()
        self.model_name = model_name
        logger.info(f"TogetherModel initialized with model: {model_name}")

    def generate_code(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            code = response.choices[0].message.content
            return code
        except Exception as e:
            logger.error(f"Together AI generation failed: {e}")
            raise
