import time

import asyncio

def read_file(filenaim):
    with open(filenaim,'r') as f:
        time.sleep(5)
        return f.read()
