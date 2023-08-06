import asyncio

async def coro():
    await asyncio.sleep(1)
    return 'Result'

async def main():
    fut = asyncio.Future()
    task = asyncio.create_task(coro())

    result = await fut

    result = await task

asyncio.run(main())