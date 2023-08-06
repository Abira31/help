import asyncio
import aiohttp

async def fetch(session,url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        urls = [
            'https://jsonplaceholder.typicode.com/posts/1',
            'https://jsonplaceholder.typicode.com/posts/2',
            'https://jsonplaceholder.typicode.com/posts/3',
        ]
        tasks = [asyncio.create_task(fetch(session,url)) for url in urls]
        result = await asyncio.gather(*tasks)
        print(result)

asyncio.run(main())