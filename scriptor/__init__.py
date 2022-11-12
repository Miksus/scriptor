from .program import Program, BaseProgram
from .process import Process, AsyncProcess, ProcessError

from . import _version
__version__ = _version.get_versions()['version']