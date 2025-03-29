
```
docekr compose build
docker compose up -d
 docker compose up -d db_pg

# without docekr in the root
uvicorn app.main:app
```
Для хранения сессии при авторизации тг, нужна создать папку в корне
```
mkdir tg_sesson
```