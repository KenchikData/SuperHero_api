
# SuperHero API

Простой REST API для работы с данными супергероев, реализованный на FastAPI с использованием асинхронного SQLAlchemy и PostgreSQL.

## Описание проекта

- При добавлении героя (**POST /hero/**) сервер обращается к внешнему SuperHero API, забирает характеристики и сохраняет их в локальной базе.
- При запросе списка героев (**GET /heroes/**) можно фильтровать по имени и числовым полям (`intelligence`, `strength`, `speed`, `power`) с операциями `=`, `>=`, `<=`.

## Технологический стек

- Python 3.12  
- FastAPI  
- SQLAlchemy (async) + asyncpg  
- PostgreSQL  
- Alembic (миграции)  
- HTTPX (внешние HTTP-запросы)  
- Docker & Docker Compose  
- pytest + pytest-asyncio  
- Makefile (шорткаты для команд)  

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/<ваш-пользователь>/SuperHero_api.git
   cd SuperHero_api
   ```

2. Скопируйте пример файла окружения и укажите токен:

   ```bash
   cp .env.example .env
   # В файле .env заполните SUPERHERO_API_TOKEN
   ```
3. Соберите и запустите все сервисы:

   ```bash
   make up
   ```
4. Перейдите в браузер по адресу:

   ```
   http://localhost:8000/docs
   ```

   чтобы открыть Swagger UI.

## Makefile — основные команды

| Команда         | Описание                                 |
| --------------- | ---------------------------------------- |
| `make up`       | Сборка и запуск контейнеров              |
| `make down`     | Остановка и удаление контейнеров и томов |
| `make build`    | Пересборка Docker-образов                |
| `make test`     | Запуск pytest внутри контейнера API      |
| `make shell`    | Bash внутри контейнера API               |
| `make logs`     | Просмотр логов всех сервисов             |
| `make db-shell` | Подключение к PostgreSQL (psql)          |

## API Эндпоинты

### 1. Добавление героя

`POST /hero/`

* **Тело запроса** (JSON):

  ```json
  { "name": "Batman" }
  ```
* **Ответ 201 Created**:

  ```json
  {
    "id": 1,
    "name": "Batman",
    "intelligence": 81,
    "strength": 40,
    "speed": 29,
    "power": 63
  }
  ```
* **Коды ошибок**:

  * `400 Bad Request` — герой уже существует в базе
  * `404 Not Found` — герой не найден во внешнем SuperHero API

### 2. Список героев и фильтрация

`GET /heroes/`

* **Query-параметры** (все опциональны):

  * `name` — точное совпадение по имени
  * `intelligence`, `strength`, `speed`, `power` — можно указать вместе с суффиксами:

    * `_{field}` — точное значение
    * `_{field}_ge` — ≥ значения
    * `_{field}_le` — ≤ значения

* **Примеры запросов**:

  ```
  GET /heroes/?strength_ge=90
  GET /heroes/?name=Hulk&power_le=100
  ```

* **Ответ 200 OK** — массив объектов героев:

  ```json
  [
    {"id":2,"name":"Hulk","intelligence":88,"strength":100,"speed":63,"power":98}
  ]
  ```

* **404 Not Found** — нет героев по заданным фильтрам

## Миграции (Alembic)

* Схема создаётся автоматически при запуске (через `Base.metadata.create_all`).
* Для ручной миграции:

  ```bash
  make shell
  alembic revision --autogenerate -m "init heroes table"
  alembic upgrade head
  ```

## Тестирование

```bash
make test
```

* Все тесты (`pytest`) проходят без ошибок и предупреждений.
* Внешние запросы к SuperHero API замоканы.

## Лицензия и автор

© 2025, Никита Арефьев

---

*Работа с внешним SuperHero API была выполнена для получения и сохранения характеристик героев.*
