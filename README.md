# Mini Tender Parser

## Как запустить
1. Клонируйте репозиторий
2. `python -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python main.py --max 50 --output tenders.csv`

## Что использовал
- requests+BeautifulSoup – парсинг
- pandas – экспорт
- typer – CLI
- FastAPI – REST (опционально)

## Что бы улучшил
- Добавить обработку ошибок и ретраи
- Использовать асинхронные запросы (aiohttp)
- Docker-образ
- Unit-тесты