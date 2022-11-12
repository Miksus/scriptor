from typing import Union
import io

def to_string(s:Union[str, bytes], **kwargs) -> str:
    if isinstance(s, str):
        return s
    elif isinstance(s, io.BufferedReader):
        s = s.read()
    s = s.decode(**kwargs)
    # Turn "\r\n" to "\n" (Windows)
    return "\n".join(s.splitlines())

def to_bytes(s:Union[str, bytes], **kwargs) -> bytes:
    if isinstance(s, bytes):
        return s
    return s.encode(**kwargs)