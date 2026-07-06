from fastapi import FastAPI

from app.db.session import check_database_connection

app = FastAPI(
    title="Tennis Prediction System",
    version="0.1.0",
)


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