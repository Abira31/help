import asyncio

async def some_task():
    await asyncio.sleep(1)
    return 'Task completed'

async def main():
    task = asyncio.create_task(some_task())
    task.add_done_callback(callback)
    print(task.done())
    task.cancel()
    print(task.done())
    try:
        await task
    except asyncio.CancelledError:
        print('Task was cancelled')
    else:
        print(task.result())
    print(task.exception())
    task.set_result('New result')
    print(task.result())
    task.set_exception(ValueError('New error'))


def callback(future):
    print('Callback called')

asyncio.run(main())