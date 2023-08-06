import asyncio
import aiofiles

async def read_file(filename):
    async with aiofiles.open(filename,'r') as f:
        content = await f.read()
        return content

async def main():
    print("start")
    result = await asyncio.gather(read_file('example.txt'))
    print("end",result)

asyncio.run(main())