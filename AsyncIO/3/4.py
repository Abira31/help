import httpx
import asyncio

adrs =  "https://langa.pl/crawl/"

async def progress(
        url:str,
        algo:asyncio.Condition[...,asyncio.Condition]
):
    asyncio.create_task(
        algo(url),
        name=url
    )