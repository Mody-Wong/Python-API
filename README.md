# Running Training Plan API

A production-style FastAPI backend for creating, storing, and adapting personalised running training plans.

The goal of this project is to let runners submit their race goal, current fitness, availability, and preferences, then receive a structured training plan that can be retrieved and recalculated as circumstances change.

This repository is also designed to demonstrate how backend engineering patterns commonly used in Java Spring services translate into Python and FastAPI.

## Tech Stack

- Python
- FastAPI
- Pytest

## Current Features

- Health check endpoint
- Protected authenticated user endpoint
- Create a training plan in memory
- Retrieve an in-memory training plan by ID
- List the authenticated user's in-memory training plans
- Auth0 configuration and token validation helper

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

Contains legacy SQLAlchemy database models. These are not used by the mounted API on this branch.

`database/`

Contains legacy database setup. No mounted FastAPI route depends on it on this branch.

`core/`

Contains application configuration, including environment-driven Auth0 settings.

`migrations/`

Contains legacy Alembic migration files. These are not required while this branch is running without a database.

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
  -> Pydantic response schema
  -> JSON response
```

Example:

```text
POST /training-plans
  -> routers/training_plans.py
  -> services/training_plan_service.py
  -> TrainingPlanResponse
```

## API Endpoints

### Health

```http
GET /health
```

Checks that the API is running.

### Auth

```http
GET /me
```

Returns selected claims from a valid Auth0 bearer token.

### Training Plans

```http
POST /training-plans
```

Creates and stores a training plan in memory.

Requires an Auth0 bearer token. The plan is associated with the token's `sub`
claim.

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
GET /training-plans
```

Lists the authenticated user's in-memory training plans.

Requires an Auth0 bearer token. Only plans associated with the token's `sub`
claim are returned.

```http
GET /training-plans/{plan_id}
```

Retrieves an in-memory training plan by ID.

Requires an Auth0 bearer token. A plan is only returned to the user who created
it.

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

### 3. Start The API

```bash
.venv/bin/uvicorn main:app --reload
```

Open the interactive API docs:

```text
http://127.0.0.1:8000/docs
```

## Testing

Run all tests:

```bash
.venv/bin/python -m pytest
```

The test suite currently includes:

- Router tests for the active API contract
- Service tests for in-memory training plan behavior

## Deployment Notes

This project is intended to be deployable to AWS Elastic Beanstalk.

Deployment expectations:

- Elastic Beanstalk runs the FastAPI app using the root `Procfile`
- Runtime dependencies are installed from `requirements.txt`
- Auth0 configuration is provided through environment variables

Before deploying:

```bash
.venv/bin/python -m pytest
```

After deployment, verify:

```text
GET /health
```

## Useful Commands

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
