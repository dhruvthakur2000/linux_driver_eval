import os
import argparse
from dotenv import load_dotenv
from src.models.model_registry import together_models, get_model
from src.utils import extract_code_blocks, save_generated_code
from src.logger import logger
from src.errors import PromptFileError, ModelLoadError ,CodeGenerationError

load_dotenv()
TOGETHER_API_KEY=os.getenv("TOGETHER_API_KEY")


def read_prompt(path):
    try:
        with open(path, "r") as f:
            prompt=f.read()
            logger.info(f"Loaded prompt form {path}")
            return prompt
    except Exception as e:
        logger.error(f"Failed to read prompt:{e}")
        raise PromptFileError(str(e))
    

def main():
    parser= argparse.ArgumentParser(description="Run prompt with the selected model")
    
    parser.add_argument("--prompt","--p",
                        type=str,
                        required=True,
                        help="path to prompt file")
    
    parser.add_argument("--model", "--m",
                        type=str,
                        choices=list(together_models.keys()),
                        help="Choose the model to use"
                        )

    parser.add_argument("--output","--o",
                        type=str,
                        help="Option output path for code to be saved") 

    args=parser.parse_args()
    if not args.output:
        args.output = "generated_code"
    

    try:
            prompt_path = os.path.join("prompts", args.prompt)
            prompt = read_prompt(prompt_path)

            logger.info(f"model selected: {args.model}")
            logger.info(f"The prompt selected from :{args.prompt}")

            model = get_model(args.model)

            try:
                response = model.generate_code(prompt)
                logger.info(" Response received from Together AI.")
                logger.debug(f"Raw Response:\n{response}")

            except Exception as model_error:
                raise ModelLoadError(f"Together AI generation failed: {model_error}")

            code = extract_code_blocks(response)
            save_generated_code(args.model, code, output_path=args.output)
            logger.info("Code generation complete.")

    except (PromptFileError, ModelLoadError, Exception) as e:
        logger.error(f" Pipeline failed: {e}")


if __name__ == "__main__":
    main()