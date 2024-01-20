# KYC
<hr>
<h3>Создание миграций</h3>
https://tortoise.github.io/migration.html#usage
<h4>1. Если миграции ранее не созданы</h4>

- инициализируем aerich:

```bash
aerich init -t src.config.settings.TORTOISE_ORM --location ./db/migrations
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

<hr>
<h3>Создание пользователей</h3>

- После создания базы данных, при создании пользователя через эндпоинт, 
первым будет создан суперпользователь (права администратора и персонала)! 
Все последующие без прав администратора и персонала
- для создания тестовых пользователь при помощи скрипта запустите команду:

```bash
python3 scripts/createusers.py
```

<hr>
<h3>Запуск сервера</h3>

- для доступа только на локальной машине

```bash
uvicorn main:app --reload
```

- для получения доступа по сети

```bash
uvicorn main:app --reload --port 8000 --host 0.0.0.0
```

- запуск Celery

```bash
celery --app=src.app.worker.app worker --concurrency=1 --loglevel=DEBUG
```