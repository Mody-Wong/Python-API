# Running Training Plan API

A production-style FastAPI backend for creating, storing, and adapting personalised running training plans.

The goal of this project is to let runners submit their race goal, current fitness, availability, and preferences, then receive a structured training plan that can be retrieved and recalculated as circumstances change.

This repository is also designed to demonstrate how backend engineering patterns commonly used in Java Spring services translate into Python and FastAPI.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker Compose
- Pytest

## Current Features

- Health check endpoint
- Database health check endpoint
- Create a training plan
- Retrieve a training plan by ID
- PostgreSQL persistence
- Alembic database migrations
- Router-level and service-level tests

## Architecture

The project follows a layered backend structure:

```text
main.py
routers/
services/
schemas/
models/
database/
core/
tests/
```

### Folder Responsibilities

`routers/`

Defines HTTP endpoints. This layer handles request routing, status codes, dependency injection, and response models.

`services/`

Contains business logic. Routers delegate to services instead of directly handling application behavior.

`schemas/`

Contains Pydantic request and response models. These are similar to DTOs in a Spring application.

`models/`

Contains SQLAlchemy database models. These are similar to JPA entities.

`database/`

Contains database setup, SQLAlchemy session configuration, and the `get_db` dependency used by FastAPI routes.

`core/`

Contains application configuration, including environment-driven settings such as the database URL.

`migrations/`

Contains Alembic migration files. These track database schema changes over time.

`tests/`

Contains automated tests organized by application layer.

## Spring To FastAPI Mapping

| Spring Boot | FastAPI Project |
| --- | --- |
| Controller | Router |
| Service | Service |
| DTO | Pydantic schema |
| JPA Entity | SQLAlchemy model |
| Repository / EntityManager | SQLAlchemy session |
| Flyway / Liquibase | Alembic |
| Dependency Injection | `Depends(...)` |

## Request Flow

```text
Client
  -> FastAPI app
  -> Router
  -> Service
  -> SQLAlchemy session
  -> PostgreSQL
  -> Pydantic response schema
  -> JSON response
```

Example:

```text
POST /training-plans
  -> routers/training_plans.py
  -> services/training_plan_service.py
  -> models/training_plan.py
  -> PostgreSQL
  -> TrainingPlanResponse
```

## API Endpoints

### Health

```http
GET /health
```

Checks that the API is running.

```http
GET /health/db
```

Checks that the API can connect to the database.

### Training Plans

```http
POST /training-plans
```

Creates and stores a training plan.

Example request:

```json
{
  "race_type": "half_marathon",
  "race_date": "2026-09-20",
  "experience_level": "beginner",
  "days_per_week": 4
}
```

Example response:

```json
{
  "id": 1,
  "race_type": "half_marathon",
  "race_date": "2026-09-20",
  "experience_level": "beginner",
  "days_per_week": 4,
  "status": "draft"
}
```

```http
GET /training-plans/{plan_id}
```

Retrieves a stored training plan by ID.

## Local Development

### 1. Create And Activate A Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -r requirements-dev.txt
```

### 3. Start PostgreSQL

```bash
docker compose up -d
```

Check the container:

```bash
docker compose ps
```

### 4. Run Database Migrations

```bash
.venv/bin/alembic upgrade head
```

### 5. Start The API

```bash
.venv/bin/uvicorn main:app --reload
```

Open the interactive API docs:

```text
http://127.0.0.1:8000/docs
```

## Database

Local PostgreSQL is provided by Docker Compose.

Default local connection:

```text
postgresql+psycopg://running_user:running_password@localhost:5432/running_plan_db
```

Environment variable:

```text
DATABASE_URL
```

See `.env.example` for the expected format.

## Testing

Run all tests:

```bash
.venv/bin/python -m pytest
```

The test suite currently includes:

- Router tests for API contracts
- Service tests for business logic
- Validation tests for invalid request data

Training plan tests use an in-memory SQLite database override, so they do not require Docker or PostgreSQL to be running.

## Useful Commands

Start PostgreSQL:

```bash
docker compose up -d
```

Stop PostgreSQL:

```bash
docker compose down
```

Run migrations:

```bash
.venv/bin/alembic upgrade head
```

Check current migration:

```bash
.venv/bin/alembic current
```

Run the app:

```bash
.venv/bin/uvicorn main:app --reload
```

Run tests:

```bash
.venv/bin/python -m pytest
```

## Roadmap

- Add runner profile inputs
- Add race goal details
- Add availability and training preferences
- Generate multi-week structured training plans
- Add plan update and recalculation endpoints
- Add richer domain rules for training load and recovery
- Add AWS Elastic Beanstalk deployment configuration
- Use Amazon RDS for production PostgreSQL
