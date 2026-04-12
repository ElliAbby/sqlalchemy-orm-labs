# Запуск

1. Создать `.env`
```text
DB_NAME=your_name_to_db
DB_ECHO=False
```

2. Загрузка зависимостей
```bash
poetry install
```

3. Запуск проекта

Для императивного подхода в синхронном режиме
```bash
poetry run python src/main.py --core --sync
```

Для декларативного подхода в синхронном режиме
```bash
poetry run python src/main.py --orm --sync
```
