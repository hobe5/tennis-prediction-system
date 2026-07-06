from fastapi import FastAPI

from app.api.routes.players import router as players_router
from app.db.session import check_database_connection

app = FastAPI(
    title="Tennis Prediction System",
    version="0.1.0",
)

app.include_router(players_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "system": "tennis-prediction-system",
        "version": "0.1.0",
    }


@app.get("/db-health")
def database_health_check():
    check_database_connection()

    return {
        "status": "ok",
        "database": "connected",
    }