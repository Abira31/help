import asyncio

async def long_operation():
    print("Start")
    await asyncio.sleep(5)
    print("End")

async def main():
    print("start_task")
    task = asyncio.create_task(long_operation())
    await task
    print("end_task")

asyncio.run(main())