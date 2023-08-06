import asyncio
import datetime

def print_now():
    print(datetime.datetime.now())

loop = asyncio.get_event_loop()
loop.call_soon(print_now)
loop.run_until_complete(asyncio.sleep(5))