# Запуск

1. Создать `.env`
```text
DB_URL=your_path_to_db
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
