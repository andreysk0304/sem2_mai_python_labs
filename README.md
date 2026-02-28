# Отчёт по лабораторной работе №1 (task platform)

---

**ФИО:** Курноскин Андрей Сергеевич  
**Группа:** М8О-102БВ-25

---

## Использование

### Тесты

для запуска локально

установка зависимостей
```bash 
pip install -r requirements.txt
```
запуск pytest, без покрытия
```bash
pytest tests/ -v
```
запуск petest, с покрытием
```bash
pytest tests/ -v --cov=task_platform --cov-report=term-missing
```
( Запускать апи не нужно т.к работа с ним замокана или использует локальные клинеты )

### Демо запуск

```bash
uvicorn task_platform.api.main:app --reload --port 8000
python run_demo.py
```

Чтобы демо не упал, сначала запускаем API, а затем демо работу платформы

**Docker**

Одной командой поднять API и запустить демо (API остаётся работать, демо выполнится один раз после готовности API):

```bash
docker compose up
```

Только API (в фоне — `docker compose up -d api`):

```bash
docker compose up api
```

Только один прогон демо (API должен быть уже запущен):

```bash
docker compose run --rm demo
```
# sem2_mai_python_labs
