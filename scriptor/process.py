import asyncio
from re import S
import subprocess
from abc import abstractmethod
from typing import Any, Union
from .utils import to_string, to_bytes

def _raise_for_error(proc:Union[subprocess.Popen, asyncio.subprocess.Process], cmd):
    returncode = proc.returncode
    if returncode:
        stdout = to_string(proc.stdout)
        stderr = to_string(proc.stderr)
        raise ProcessError(
            returncode=returncode, 
            cmd=cmd,
            output=stdout,
            stderr=stderr,
        )

def _raise_for_error(returncode, cmd, stdout, stderr):
    if returncode:
        stdout = to_string(stdout)
        stderr = to_string(stderr)
        raise ProcessError(
            returncode=returncode, 
            cmd=cmd,
            output=stdout,
            stderr=stderr,
        )

class ProcessError(subprocess.CalledProcessError):

    def __str__(self):
        return self.stderr

class BaseProcess:

    def __init__(self, proc, cmd=None, input_parser=None, output_parser=None):
        self._proc = proc
        self.cmd = cmd

        self.input_parser = input_parser
        self.output_parser = output_parser

    def write(self, s):
        parser = self.input_parser
        if parser is not None:
            s = parser(s)
        self._proc.stdin.write(to_bytes(s))
        self._proc.stdin.close()

    def _parse_output(self, s):
        parser = self.output_parser
        if parser is None:
            return s
        return parser(s)

    @property
    def finished(self):
        return self.returncode is not None

    @property
    def running(self):
        return self.returncode is None

# Copied from Process/Popen

    @property
    def returncode(self) -> int:
        return self._proc.returncode

    @property
    def stdin(self):
        return self._proc.stdin

    @property
    def stdout(self):
        return self._proc.stdout

    @property
    def stderr(self):
        return self._proc.stderr

    def send_signal(self, signal):
        self._proc.send_signal(signal)

    def terminate(self):
        self._proc.terminate()

    def kill(self):
        self._proc.kill()

    def __repr__(self):
        return repr(self._proc)

class Process(BaseProcess):
    _proc: subprocess.Popen

    @property
    def returncode(self) -> int:
        self._proc.poll()
        return self._proc.returncode

    def wait(self):
        self._proc.wait()

    def communicate(self, input=None):
        self._proc.communicate(input=input)

    def read(self):
        stdout = self._proc.stdout.read()
        return self._parse_output(stdout)

    def read_err(self):
        stderr = self._proc.stderr.read()
        return stderr

    def raise_for_return(self):
        _raise_for_error(
            returncode=self._proc.returncode, 
            cmd=self.cmd,
            stdout=self._proc.stdout,
            stderr=self._proc.stderr,
        )


class AsyncProcess(BaseProcess):
    _proc: asyncio.subprocess.Process
    _stdout: bytes
    _stderr: bytes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stdout = None
        self._stderr = None

    async def wait(self):
        await self._proc.wait()

    async def communicate(self, input=None):
        self._proc.communicate(input=input)

    async def read(self):
        stdout = await self._get_stdout()
        return self._parse_output(stdout)

    async def read_bytes(self):
        return await self._get_stdout()

    async def read_err(self):
        stderr = self._get_stderr()
        return stderr

    async def raise_for_return(self):
        _raise_for_error(
            returncode=self._proc.returncode, 
            cmd=self.cmd,
            stdout=await self._get_stdout(),
            stderr=await self._get_stderr(),
        )

    async def _get_stdout(self):
        stream = self._proc.stdout
        consumed = self._stdout is not None
        if not consumed:
            self._stdout = await stream.read()
        return self._stdout

    async def _get_stderr(self):
        stream = self._proc.stderr
        consumed = self._stderr is not None
        if not consumed:
            self._stderr = await stream.read()
        return self._stderr
