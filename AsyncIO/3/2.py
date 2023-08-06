import datetime
import asyncio

def print_now():
    print(datetime.datetime.now())

async def keep_pring(name:str="") -> None:
    while True:
        print(name,end=" ")
        print_now()
        try:
            await asyncio.sleep(.5)
        except asyncio.CancelledError:
            print(name,"was cancelled")
            break

# async def async_main():
#     await asyncio.gather(
#         keep_pring("First"),
#         keep_pring("Second"),
#         keep_pring("Thied")
#     )

async def async_main():
    try:
        await asyncio.wait_for(
            asyncio.gather(
                keep_pring("First"),
                keep_pring("Second"),
                keep_pring("Thied")
            ),3
        )
    except asyncio.TimeoutError:
        print("oops, time's up!")

asyncio.run(async_main())