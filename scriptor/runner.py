from abc import abstractmethod
import asyncio
from typing import Union, Generator
import subprocess

from .process import ProcessError, Process, AsyncProcess, _raise_for_error

class Runner:
    "Command-line runner"

    def __init__(self, output=str):
        self.kwargs = {
            'stdin': subprocess.PIPE,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
        }
        self.output = output

    def start_program(self, cmd, input=None, timeout=None, **kwargs) -> Process:
        "Start the process"
        kwds = self.kwargs.copy()
        kwds.update(kwargs)
        proc = Process(subprocess.Popen(cmd, **kwds), cmd=cmd)
        if input is not None:
            proc.write(input)
        return proc

    async def start_program_async(self, cmd, input=None, timeout=None, **kwargs) -> AsyncProcess:
        "Start the process"
        kwds = self.kwargs.copy()
        kwds.pop("text", None) # asyncio.Process does not accept text for some reason
        #kwds.pop("stdin", None)
        kwds.update(kwargs)

        proc = AsyncProcess(
            await asyncio.create_subprocess_exec(*cmd, **kwds), 
            cmd=cmd
        )
        if input is not None:
            proc.write(input)
        return proc

    def run_process_sync(self, cmd, input=None, timeout=None, **kwargs) -> bytes:
        "Run process and return the output"
        kwds = self.kwargs.copy()
        kwds.pop("stdin", None)
        kwds.update(kwargs)

        proc = subprocess.run(cmd, input=input, timeout=timeout, **kwds)
        _raise_for_error(proc.returncode, cmd=cmd, stdout=proc.stdout, stderr=proc.stderr)
        return proc.stdout

    async def run_process_async(self, cmd, input=None, timeout=None, **kwargs) -> bytes:
        "Run process async"
        proc = await self.start_program_async(cmd, input=input, **kwargs)
        await asyncio.wait_for(proc.wait(), timeout=timeout)

        await proc.raise_for_return()
        out = await proc.get_stdout()

        return out

    def run_process_iter(self, cmd, input=None, **kwargs) -> Generator[bytes, None, None]:
        "Run and iterate the process output"
        proc = self.start_program(cmd, input=input, **kwargs)

        while True:
            line = proc.stdout.readline()
            if line in (b'', ''):
                break
            yield line
        proc.stdout.close()
        _raise_for_error(proc.returncode, cmd=cmd, stdout=proc.stdout, stderr=proc.stderr)

    def _write_stdin(self, pipe:subprocess.Popen, stdin):
        try:
            pipe.stdin.write(stdin)
        except (BrokenPipeError, OSError):
            # Popen._write_stdin also ignores these errors
            pass

DEFAULT_RUNNER = Runner()

run_process_sync = DEFAULT_RUNNER.run_process_sync
run_process_async = DEFAULT_RUNNER.run_process_async
run_process_iter = DEFAULT_RUNNER.run_process_iter
start_process = DEFAULT_RUNNER.start_program
start_process_async = DEFAULT_RUNNER.start_program_async