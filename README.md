# Running Training Plan API

A production-style FastAPI backend for creating, storing, and adapting personalised running training plans.

The goal of this project is to let runners submit their race goal, current fitness, availability, and preferences, then receive a structured training plan that can be retrieved and recalculated as circumstances change.

This repository is also designed to demonstrate how backend engineering patterns commonly used in Java Spring services translate into Python and FastAPI.

## Tech Stack

- Python
- FastAPI
- DynamoDB
- Boto3
- Pytest

## Current Features

- Health check endpoint
- Database health check endpoint
- Create a training plan
- Retrieve a training plan by ID
- DynamoDB persistence
- Router-level and service-level tests

## Architecture

The project follows a layered backend structure:

```text
main.py
routers/
services/
schemas/
repositories/
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

`repositories/`

Contains persistence adapters. The current implementation stores and retrieves training plans from DynamoDB.

`core/`

Contains application configuration, including environment-driven settings such as the database URL.

`tests/`

Contains automated tests organized by application layer.

## Spring To FastAPI Mapping

| Spring Boot | FastAPI Project |
| --- | --- |
| Controller | Router |
| Service | Service |
| DTO | Pydantic schema |
| JPA Entity | Domain model / persisted item |
| Repository | DynamoDB repository |
| Flyway / Liquibase | DynamoDB table provisioning |
| Dependency Injection | `Depends(...)` |

## Request Flow

```text
Client
  -> FastAPI app
  -> Router
  -> Service
  -> DynamoDB repository
  -> DynamoDB
  -> Pydantic response schema
  -> JSON response
```

Example:

```text
POST /training-plans
  -> routers/training_plans.py
  -> services/training_plan_service.py
  -> repositories/training_plan_repository.py
  -> DynamoDB
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
  "id": "3f0a4a2a-7e2f-4d4a-8d84-1f8d9552e8f1",
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

### 3. Configure DynamoDB

Create a DynamoDB table with:

```text
Table name: training-plans
Partition key: id
Partition key type: String
```

For AWS deployment, make sure the Elastic Beanstalk instance role has permission to read and write this table.

### 4. Start The API

```bash
.venv/bin/uvicorn main:app --reload
```

Open the interactive API docs:

```text
http://127.0.0.1:8000/docs
```

## DynamoDB

The API stores training plans in DynamoDB.

Environment variables:

```text
AWS_REGION=eu-west-2
TRAINING_PLANS_TABLE_NAME=training-plans
DYNAMODB_ENDPOINT_URL=
```

`DYNAMODB_ENDPOINT_URL` is optional. It can be used for local DynamoDB tooling; leave it unset in AWS.

## Testing

Run all tests:

```bash
.venv/bin/python -m pytest
```

The test suite currently includes:

- Router tests for API contracts
- Service tests for business logic
- Validation tests for invalid request data

Training plan tests use an in-memory fake repository, so they do not require AWS or DynamoDB to be running.

## Deployment Notes

This project is intended to be deployable to AWS Elastic Beanstalk with DynamoDB as the persistence layer.

Deployment expectations:

- Elastic Beanstalk runs the FastAPI app using the root `Procfile`
- Runtime dependencies are installed from `requirements.txt`
- DynamoDB table configuration is provided through environment variables
- The Elastic Beanstalk instance role must have DynamoDB table permissions

Before deploying:

```bash
.venv/bin/python -m pytest
```

Set these environment variables in Elastic Beanstalk:

```text
AWS_REGION=eu-west-2
TRAINING_PLANS_TABLE_NAME=training-plans
```

After deployment, verify:

```text
GET /health
GET /health/db
POST /training-plans
GET /training-plans/{plan_id}
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
- Add infrastructure-as-code for DynamoDB table provisioning
