# 🏨 Booking.com API Clone (Mini Version)

[Русский](#russian) | [English](#english)

---

<a name="russian"></a>
## 🇷🇺 Описание проекта

**Booking.com API Clone** — это асинхронное RESTful API веб-приложение для системы бронирования отелей и номеров, построенное с использованием современных стандартов разработки на Python. 

Проект разработан в качестве демонстрационного пет-проекта для демонстрации навыков проектирования масштабируемой backend-архитектуры, асинхронного взаимодействия с СУБД PostgreSQL и реализации алгоритмов проверки доступности номеров без овербукинга.

### 🛠 Стек технологий
- **Backend:** Python 3.12, FastAPI
- **Database & ORM:** PostgreSQL, SQLAlchemy 2.0 (Async Session), asyncpg
- **Security & Auth:** PyJWT, pwdlib (Argon2), OAuth2 Password Bearer
- **Validation & Settings:** Pydantic v2, Pydantic Settings
- **DevOps & Infrastructure:** Docker, Docker Compose

### 🏗 Архитектура и особенности реализации
- **Layered Architecture (Repository + Service Pattern):**
  - `Endpoints` — обработка HTTP-запросов и маршрутизация.
  - `Services` — изолированная бизнес-логика (расчёт стоимости, проверки доступности).
  - `Repositories` — абстракция слоя работы с БД (CRUD и сложные SQLAlchemy-запросы).
- **Алгоритм предотвращения овербукинга:** Проверка пересечения дат бронирований (`date_from < new_date_to AND date_to > new_date_from`) на уровне базы данных с учётом общего количества доступных номеров конкретной категории.
- **Безопасность:** Хеширование паролей с помощью стойкого алгоритма **Argon2**, авторизация через **JWT** (access-токены в HttpOnly Cookie и Authorization header).

### 🚀 Быстрый запуск через Docker Compose

1. **Клонировать репозиторий:**
   ```bash
   git clone [https://github.com/Artemchirkov/booking_copy.git](https://github.com/Artemchirkov/booking_copy.git)
   cd booking_copy

2. Создать файл окружения .env в корне проекта:

  ```
  DB_HOST=db
  DB_PORT=5432
  DB_USER=booking_user
  DB_PASS=booking_password
  DB_NAME=booking_db
  
  SECRET_KEY=YOUR_SUPER_SECRET_KEY_HERE
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=1440
  ```

3. Запустить контейнеры:
  ```Bash
  docker compose up --build -d
  ```
4. Документация API:
После запуска Swagger UI доступен по адресу: http://localhost:8000/docs
