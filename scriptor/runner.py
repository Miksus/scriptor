import asyncio
import subprocess

DEFAULT_KWARGS = {
    'stdout': subprocess.PIPE,
    'stderr': subprocess.PIPE,
    'text': True
}

class Runner:
    "Command-line runner"

    def __init__(self):
        self.kwargs = {
            'stdin': subprocess.PIPE,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'text': True
        }

    def run_process_sync(self, cmd, stdin=None, timeout=None, **kwargs):
        kwds = self.kwargs.copy()
        kwds.update(kwargs)

        pipe = subprocess.Popen(cmd, **kwds)
        try:
            outs, errs = pipe.communicate(input=stdin, timeout=timeout)
        except subprocess.TimeoutExpired:
            # https://docs.python.org/3.3/library/subprocess.html#subprocess.Popen.communicate
            pipe.kill()
            outs, errs = pipe.communicate()
            raise
        self._raise_for_error(pipe, errs)
        return outs

    async def run_process_async(self, cmd, stdin=None, timeout=None, **kwargs):
        kwds = self.kwargs.copy()
        kwds.pop("text") # asyncio.Process does not accept text for some reason
        kwds.update(kwargs)

        pipe = await asyncio.create_subprocess_exec(*cmd, stdin=stdin, **kwds)
        await asyncio.wait_for(pipe.wait(), timeout=timeout)
        self._raise_for_error(pipe)
        out = await pipe.stdout.read()
        if hasattr(out, "decode"):
            out = out.decode("utf-8", errors="ignore")
        return out

    def run_process_iter(self, cmd, stdin=None, **kwargs):
        kwds = self.kwargs.copy()
        kwds.update(kwargs)
        pipe = subprocess.Popen(cmd, **kwds)
        if stdin is not None:
            self._write_stdin(pipe, stdin)

        while True:
            line = pipe.stdout.readline()
            if line in (b'', ''):
                break
            yield line
        pipe.stdout.close()
        self._raise_for_error(pipe)

    def _raise_for_error(self, popen:subprocess.Popen, errs=None):
        while popen.returncode is None:
            popen.wait()
        return_code = popen.returncode
        if return_code != 0:
            if errs is None:
                errs = popen.stderr.read()
            if hasattr(errs, "decode"):
                errs = errs.decode("utf-8", errors="ignore")
            raise OSError(f"Failed running command ({return_code}): \n{errs}")

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