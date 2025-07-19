import subprocess
import os
from typing import Tuple

mock_header_dir=os.path.join(os.path.dirname(__file__),'..','mock_linux_headers')
gen_code_dir=os.path.join(os.path.dirname(__file__),'..','generated_code')


def compile_driver(code: str, filename:str='char_driver.c')-> Tuple[bool,str]:
    