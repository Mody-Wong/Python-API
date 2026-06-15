from fastapi import FastAPI

from routers import health, me, training_plans

app = FastAPI(title="Project 1 API")

app.include_router(health.router)
app.include_router(me.router)
app.include_router(training_plans.router)

