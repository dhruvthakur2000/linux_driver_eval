import argparse
import os
from src.models.mistral import MistralModel
from src.errors import ModelLoadError, CodeGenerationError, PromptFileError
from src.logger import get_logger
from src.models.phi import PhiModel
from src.models.mistral import MistralModel
from src.models.codegemma import CodeGemmaModel
from src.models.starcoder import StarCoderModel
from src.models.deepseek import DeepSeekModel

logger=get_logger("code_runner")

MODEL_REGISTRY = {
    "phi": PhiModel,
    "mistral": MistralModel,
    "codegemma": CodeGemmaModel,
    "starcoder": StarCoderModel,
    "deepseek": DeepSeekModel
}


def read_prompt(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read prompt:{e}")
        raise PromptFileError(str(e))
    

def save_generated_code(output_path,code):
    try:
        os.makedirs(os.path.dirname(output_path),exist_ok=True)
        with open(output_path,"w") as f:
            f.write(code)
            logger.info(f"saved the generated code at:{output_path}")
    except Exception as e:
        logger.error("could not save the generated code")
        raise CodeGenerationError

def main():
    parser= argparse.ArgumentParser(description="Run prompt with the selected model")
    
    parser.add_argument("--prompt","--p",
                        type=str,
                        required=True,
                        help="path to prompt file")
    
    parser.add_argument("--model", "--m",
                        type=str,
                        choices=list(MODEL_REGISTRY.keys()),
                        help="Choose the model to use"
                        )

    parser.add_argument("--output","--o",
                        type=str,
                        help="Option output path for code to be saved") 

    args=parser.parse_args()
    
    logger.info(f"model selected:{args.model}")
    logger.info(f"The prompt selected from :{args.prompt}")
      

    prompt=read_prompt(args.prompt)
    
    try:
        model_class = MODEL_REGISTRY.get(args.model)
        model_instance = model_class()
    except Exception as e:
        logger.error(f"Failed to initialize model: {e}")
        raise ModelLoadError(str(e))

    try:
        logger.info("⚙ Generating code...")
        code = model_instance.generate_code(prompt)
    except Exception as e:
        logger.error(f"Code generation failed: {e}")
        raise CodeGenerationError(str(e))
    
    # setting up the output path
    prompt_name = os.path.splitext(os.path.basename(args.prompt))[0]
    default_output = os.path.join("generated_code", f"{args.model}_{prompt_name}.c")
    output_path = args.output if args.output else default_output

    save_generated_code(output_path, code)
    logger.info("Code generation pipeline completed.")


if __name__=="__main__":
    main()
