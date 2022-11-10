import asyncio
import subprocess

DEFAULT_KWARGS = {
    'stdout': subprocess.PIPE,
    'stderr': subprocess.PIPE,
    'text': True
}

def _raise_for_error(popen:subprocess.Popen, errs=None):
    while popen.returncode is None:
        popen.wait()
    return_code = popen.returncode
    if return_code != 0:
        if errs is None:
            errs = popen.stderr.read()
        if hasattr(errs, "decode"):
            errs = errs.decode("utf-8", errors="ignore")
        raise OSError(f"Failed running command ({return_code}): \n{errs}")

async def run_process_async(cmd, timeout=None, **kwargs):
    kwds = DEFAULT_KWARGS.copy()
    kwds.pop("text") # asyncio.Process does not accept text for some reason
    kwds.update(kwargs)

    pipe = await asyncio.create_subprocess_exec(*cmd, **kwds)
    await asyncio.wait_for(pipe.wait(), timeout=timeout)
    _raise_for_error(pipe)
    out = await pipe.stdout.read()
    if hasattr(out, "decode"):
        out = out.decode("utf-8", errors="ignore")
    return out

def run_process_sync(cmd, timeout=None, **kwargs):
    kwds = DEFAULT_KWARGS.copy()
    kwds.update(kwargs)

    pipe = subprocess.Popen(cmd, **kwds)
    try:
        outs, errs = pipe.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        # https://docs.python.org/3.3/library/subprocess.html#subprocess.Popen.communicate
        pipe.kill()
        outs, errs = pipe.communicate()
        raise
    _raise_for_error(pipe, errs)
    return outs

def run_process_iter(cmd, **kwargs):
    kwds = DEFAULT_KWARGS.copy()
    kwds.update(kwargs)
    pipe = subprocess.Popen(cmd, **kwds)
    while True:
        line = pipe.stdout.readline()
        if line in (b'', ''):
            break
        yield line 
    pipe.stdout.close()
    _raise_for_error(pipe)
