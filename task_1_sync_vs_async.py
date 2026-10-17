"""
Задание 1. Синхронно vs асинхронно.

Разница: синхронные запросы идут строго по очереди, время складывается;
асинхронные выполняются конкурентно (перекрываются по времени ожидания сети),
поэтому суммарное время заметно меньше.

Проверенное время:
sync: 4.49s
async: 0.80s
"""

import asyncio
import time
import httpx
import requests

URLS = [f"https://picsum.photos/seed/{i}/800/600" for i in range(20)]

def timed(label, fn, *args):
    start = time.perf_counter()
    fn(*args)
    print(f"{label}: {time.perf_counter() - start:.2f}s")

def sync_main():
    for url in URLS:
        requests.get(url)

async def fast_main():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [client.get(url) for url in URLS]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    timed("sync", sync_main)
    timed("async", lambda: asyncio.run(fast_main()))
