from typing import Union
from pathlib import Path
from scriptor import Program
import sys
import platform


class Python(Program):

    def __init__(self, interpreter, *args, **kwargs):
        super().__init__(interpreter, *args, **kwargs)

    def run_code(self, code:str):
        return self(c=code)

    def run_module(self, module:str):
        return self(m=module)

    def run_script(self, script:Union[str, Path], *args, **kwargs):
        return self(script, *args, **kwargs)

    @property
    def version(self):
        return self("-V")

    @property
    def full_version(self):
        return self("-VV")

    @property
    def help(self):
        return self("--help")

    @staticmethod
    def _get_base_python():
        system = platform.system()
        if system == 'Linux':
            return 'python3'
        elif system == 'Windows':
            return 'python'
        else:
            return 'python3'

python = Python(Python._get_base_python())
current = Python(sys.executable)