
import subprocess
import os
from io import BytesIO, StringIO
from copy import copy
from typing import Callable, Iterable, Tuple, Union, ByteString
from typing import Any, Dict, List
from .runner import run_process_sync, run_process_async, run_process_iter, start_process, start_process_async
from .utils import to_bytes, to_string

try:
    from typing import Literal
except ImportError: # pragma: no cover
    from typing_extensions import Literal

class Input:
    "Stdin for a program"
    def __init__(self, data:Union[str, bytes]):
        self.data = data

    def read(self):
        return to_bytes(self.data)

class BaseProgram:
    "Inheritable program class"

    program:Union[str, Iterable[str]] = None
    output_type:Literal['str', 'bytes'] = 'str'
    output_parser = None

    default_kwargs = None

    long_form_threshold = 3
    short_form = "-{}"
    long_form = "--{}"

    def __init__(self, timeout=None, cwd=None, env=None, include_current_env=True, arg_form:Literal['short', '-', 'long', '--', None]=None, encoding=None):

        self.timeout = timeout
        self.env = env
        self.cwd = cwd
        self.arg_form = arg_form
        self.encoding = encoding

        self.include_current_env = include_current_env

    def __call__(self, *args, **kwargs):
        "Run the program (with given parameters)"
        cmd, stdin = self.get_command(*args, **kwargs)
        output = run_process_sync(cmd, input=stdin, **self.get_process_kwargs())
        return self.parse_output(output)

    async def call_async(self, *args, **kwargs):
        cmd, stdin = self.get_command(*args, **kwargs)
        output = await run_process_async(cmd, input=stdin, **self.get_process_kwargs())
        return self.parse_output(output)

    def get_command(self, *args, **kwargs) -> Tuple[List[str], ByteString]:
        cmd_args, stdin_args = self.parse_args(args)
        cmd_kwargs, stdin_kwargs = self.parse_kwargs(kwargs)

        cmd = cmd_args + cmd_kwargs
        if stdin_args is not None and stdin_kwargs is not None:
            stdin = stdin_args + stdin_kwargs
        else:
            stdin = stdin_args or stdin_kwargs
        return cmd, stdin

    def __iter__(self, *args, **kwargs):
        cmd, stdin = self.get_command(*args, **kwargs)
        return run_process_iter(cmd, stdin=stdin, **self.get_process_kwargs())

    def get_process_kwargs(self):
        return dict(
            timeout=self.timeout, cwd=self.cwd, encoding=self.encoding,
            env=self._get_environ()
        )

    def _get_environ(self):
        "Get environment variables"
        env = {}
        if self.include_current_env:
            env.update(os.environ)
        if self.env is not None:
            env.update(self.env)
        return env

    def parse_args(self, args:tuple) -> Tuple[List[str], ByteString]:
        stdin = None
        cmd = []
        if self.program:
            program = [self.program] if isinstance(self.program, str) else list(self.program)
            args = program + list(args)
        for arg in args:
            if isinstance(arg, Input):
                stdin = arg.read()
            else:
                cmd.append(str(arg))
        return cmd, stdin

    def parse_kwargs(self, kwargs:Dict[str, Any]) -> Tuple[List[str], ByteString]:
        kwds = {}
        if self.default_kwargs is not None:
            kwds.update(self.default_kwargs)
        kwds.update(kwargs)

        cmd = []
        for key, val in kwds.items():
            key = self._format_key(key)
            val = str(val)
            cmd += [key, val]
        return cmd, None

    def parse_output(self, output):
        cls = self.output_type
        parser = self.output_parser
        if cls in ('str', str):
            output = to_string(output)
        elif cls in ('bytes', bytes):
            output = to_bytes(output)

        if parser is None:
            if output in ('', b''):
                return None
            return output
        return parser(output)

    def _format_key(self, key:str):
        if key.startswith("-"):
            return key

        if self.arg_form is None:
            # Determine the form from length
            if len(key) >= self.long_form_threshold:
                return self.long_form.format(key)
            else:
                return self.short_form.format(key)
        elif self.arg_form in ('short', '-'):
            return self.short_form.format(key)
        elif self.arg_form in ('long', '--'):
            return self.long_form.format(key)
        else:
            return self.arg_form.format(key)

    def copy(self):
        return copy(self)

    def use(self, **kwargs) -> 'Program':
        prog = self.copy()
        for key, val in kwargs.items():
            if not hasattr(prog, key):
                raise AttributeError(f"Invalid attribute: {key}")
            setattr(prog, key, val)
        return prog

    def start(self, *args, **kwargs):
        "Start the program"
        cmd, stdin = self.get_command(*args, **kwargs)
        proc = start_process(cmd, input=stdin, **self.get_process_kwargs())
        proc.output_parser = self.parse_output
        return proc

    async def start_async(self, *args, **kwargs):
        "Start the program"
        cmd, stdin = self.get_command(*args, **kwargs)
        proc = await start_process_async(cmd, input=stdin, **self.get_process_kwargs())
        proc.output_parser = self.parse_output
        return proc

class Program(BaseProgram):
    "Command-line program"

    def __init__(self, *program, output_parser=None, output_type="str", default_kwargs=None, **kwargs):
        self.program = program
        self.output_parser = output_parser
        self.output_type = output_type

        self.default_kwargs = default_kwargs
        super().__init__(**kwargs)
