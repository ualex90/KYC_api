# KYC
<h3>Создание миграций</h3>
https://tortoise.github.io/migration.html#usage
<h4>1. Если миграции ранее не созданы</h4>
- инициализируем aerich:

```bash
aerich init -t src.config.settings.TORTOISE_ORM
```

- создаем и применяем миграции:

```bash
aerich init-db
```
</br>
<h4>2. Если нужно применить миграции</h4>

- создаем миграции

```bash
aerich migrate
```

- применяем миграции

```bash
aerich upgrade
```

<h3>Создание тестовых пользователей</h3>

```bash
python3 scripts/createusers.py
```

<h3>Запуск сервера</h3>

- для доступа только на локальной машине

```bash
uvicorn main:app --reload
```

- для получения доступа по сети

```bash
uvicorn main:app --reload --port 8000 --host 0.0.0.0
```
