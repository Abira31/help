import httpx
import asyncio
async def craw10(prefix:str,
                 url:str = ""):
    url = url or prefix
    print(f'Crawling {url}')
    client = httpx.AsyncClient()
    try:
        res = await client.get(url)
    finally:
        await client.aclose()
    for line in res.text.splitlines():
        if line.startswith(prefix):
            await craw10(prefix,line)

asyncio.run(craw10(
    "https://langa.pl/crawl/"
))

