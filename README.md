# async-url-loader
Асинхронный загрузчик URL на Python (asyncio + httpx) для демонстрации разницы между sync/async, обработки ошибок и выноса CPU-bound задач.

## Задания
- task_0_trap.py — ловушка async без параллелизма
- task_1_sync_vs_async.py — сравнение синхронного и асинхронного подхода
- task_2_robust.py — устойчивость к ошибкам и таймаутам
- task_3_cpu.py — вынос тяжёлых вычислений в отдельный процесс
- theory.md — выбор модели параллелизма для разных кейсов

## Запуск
1. Создать и активировать venv:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
