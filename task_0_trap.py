"""
Задание 0. Разминка-ловушка.

Проблема: в slow_main await вызывается внутри цикла for, поэтому запросы идут
последовательно, а не параллельно. Async не даёт ускорения, потому что
мы не запускаем задачи конкурентно.

Решение: используем asyncio.gather для параллельного запуска всех задач.
Флаг follow_redirects=True обязателен: picsum отдаёт 302, без него httpx
не следует редиректу и мы получаем короткие ответы.

Проверенные замеры:
- slow (посл.): 12.00s
- slow (испр.): 3.50s
"""

import asyncio
import time
import httpx

URLS = [f"https://picsum.photos/seed/{i}/800/600" for i in range(20)]

def timed(label, fn, *args):
    start = time.perf_counter()
    fn(*args)
    print(f"{label}: {time.perf_counter() - start:.2f}s")

async def fetch(client: httpx.AsyncClient, url: str) -> int:
    resp = await client.get(url)
    return resp.status_code

async def slow_main():
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        for url in URLS:
            await fetch(client, url)

async def slow_main_fixed():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [fetch(client, url) for url in URLS]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    timed("slow (посл.)", lambda: asyncio.run(slow_main()))
    timed("slow (испр.)", lambda: asyncio.run(slow_main_fixed()))
