import asyncio
import time

def regular_function():
    time.sleep(3)
    return 0

@asyncio.coroutine
def async_funcion():
    yield from asyncio.sleep(3)
    return 0

regular_function()