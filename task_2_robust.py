"""
Задание 2. Реальный I/O и обработка ошибок.

robust_fetch:
- таймаут 3 секунды на запрос;
- до 3 попыток с экспоненциальной паузой (1, 2, 4 секунды);
- ловит исключения httpx и возвращает статус или ошибку.

robust_main:
- запускает все запросы параллельно;
- собирает (results, errors), где errors — список (url, error).
- один битый URL не роняет остальные.


Проверенный вывод:
Успешных: 20, ошибок: 2
Ошибки: [('https://no-such-site.invalid', '[Errno 8] nodename nor servname provided, or not known'), ('https://httpbin.org/delay/10', '')]
robust: 13.75s
"""

import asyncio
import time
import httpx

URLS = (
    [f"https://picsum.photos/seed/{i}/800/600" for i in range(20)] +
    ["https://no-such-site.invalid", "https://httpbin.org/delay/10"]
)

def timed(label, fn, *args):
    start = time.perf_counter()
    fn(*args)
    print(f"{label}: {time.perf_counter() - start:.2f}s")

async def robust_fetch(client: httpx.AsyncClient, url: str):
    max_retries = 3
    timeout = 3.0
    delay = 1.0  # экспоненциальный backoff

    for attempt in range(max_retries):
        try:
            resp = await client.get(url, timeout=timeout)
            return resp.status_code, None
        except Exception as e:
            if attempt == max_retries - 1:
                return None, (url, str(e))
            await asyncio.sleep(delay)
            delay *= 2

async def robust_main():
    results = []
    errors = []

    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [robust_fetch(client, url) for url in URLS]
        outcomes = await asyncio.gather(*tasks, return_exceptions=False)

        for status, err in outcomes:
            if err is None:
                results.append(status)
            else:
                errors.append(err)

    return results, errors

if __name__ == "__main__":
    def run():
        res, errs = asyncio.run(robust_main())
        print(f"Успешных: {len(res)}, ошибок: {len(errs)}")
        if errs:
            print("Ошибки:", errs)

    timed("robust", run)
