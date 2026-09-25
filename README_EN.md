# 🏨 Booking.com API Clone

An asynchronous RESTful API for a hotel room reservation system built with modern Python development standards (FastAPI, Async SQLAlchemy 2.0, PostgreSQL, Docker).

This project serves as a showcase backend application demonstrating expertise in scalable system architecture design, async database integration, and reliable booking overlap/overbooking prevention algorithms.

---

## 🛠 Tech Stack

- **Backend:** Python 3.12, FastAPI
- **Database & ORM:** PostgreSQL, SQLAlchemy 2.0 (Async Engine & Sessions), asyncpg
- **Security & Auth:** PyJWT, pwdlib (Argon2 password hashing), OAuth2 Password Bearer
- **Validation & Settings:** Pydantic v2, Pydantic Settings
- **DevOps & Infrastructure:** Docker, Docker Compose

---

## 🏗 Architecture & Key Features

### 1. Clean Layered Architecture (Repository + Service Pattern)
- **Routers (`app/api/`):** Request handling, HTTP status codes, and Dependency Injection.
- **Services (`app/services/`):** Business logic encapsulation (price calculations, date availability checks).
- **Repositories (`app/repositories/`):** Abstract data access layer performing async SQLAlchemy 2.0 queries.
- **Schemas (`app/schemas/`):** Strict Pydantic v2 data validation for incoming requests and responses.

### 2. Reliable Overbooking Prevention
The API prevents room overbooking by running real-time date intersection queries directly at the database level using interval overlapping logic:
$$\text{date\_from} < \text{new\_date\_to} \quad \text{AND} \quad \text{date\_to} > \text{new\_date\_from}$$
Room availability is dynamically calculated against the total quota for each room category.

### 3. Production-Ready Security
- Password hashing using the state-of-the-art **Argon2** algorithm via `pwdlib`.
- Stateless **JWT Authentication** (Access tokens support both HttpOnly Cookies and standard Bearer headers).
- Input validation prevents bad booking dates (e.g., checkout before check-in or past dates).

---

## 🚀 Quick Start with Docker Compose

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone the Repository
```bash
git clone [https://github.com/Artemchirkov/booking_copy.git](https://github.com/Artemchirkov/booking_copy.git)
cd booking_copy
