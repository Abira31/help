import datetime
import asyncio
def print_now():
    print(datetime.datetime.now())

async def keep_pring(name:str="") -> None:
    while True:
        print(name,end=" ")
        print_now()
        await asyncio.sleep(.5)

async def async_main():
    try:
        await asyncio.wait_for(keep_pring('Hey'),10)
    except asyncio.TimeoutError:
        print('ooops, time')
asyncio.run(async_main())