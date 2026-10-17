"""
Задание 3. Вынос CPU-bound-вычислений.

Наблюдение:
- При прямом вызове heavy в event loop точки ticker замирают — event loop заблокирован.
- При выносе heavy в отдельный процесс (ProcessPoolExecutor) точки продолжают
  печататься — event loop остаётся отзывчивым.

Проверенные замеры:
- ....................cpu: 2.37s (точки идут непрерывно)
"""

import asyncio
import time
import hashlib
import httpx
from concurrent.futures import ProcessPoolExecutor

URLS = [f"https://picsum.photos/seed/{i}/800/600" for i in range(20)]

def timed(label, fn, *args):
    start = time.perf_counter()
    fn(*args)
    print(f"{label}: {time.perf_counter() - start:.2f}s")

def heavy(body: bytes) -> str:
    return hashlib.sha256(body * 1000).hexdigest()

async def ticker():
    while True:
        print(".", end="", flush=True)
        await asyncio.sleep(0.1)

async def cpu_main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as executor:
        ticker_task = asyncio.create_task(ticker())

        async with httpx.AsyncClient(follow_redirects=True) as client:
            responses = await asyncio.gather(*[client.get(url) for url in URLS])

            tasks = []
            for r in responses:
                tasks.append(loop.run_in_executor(executor, heavy, r.content))
            await asyncio.gather(*tasks)

        ticker_task.cancel()
        try:
            await ticker_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    timed("cpu", lambda: asyncio.run(cpu_main()))
