from fastapi import FastAPI

from app.api.routes.case_files import router as case_files_router
from app.api.routes.evidence import router as evidence_router
from app.api.routes.frozen_predictions import router as frozen_predictions_router
from app.api.routes.matches import router as matches_router
from app.api.routes.predictions import router as predictions_router
from app.api.routes.players import router as players_router
from app.api.routes.sources import router as sources_router
from app.db.session import check_database_connection

app = FastAPI(
    title="Tennis Prediction System",
    version="0.1.0",
)

app.include_router(players_router)
app.include_router(matches_router)
app.include_router(predictions_router)
app.include_router(sources_router)
app.include_router(evidence_router)
app.include_router(frozen_predictions_router)
app.include_router(case_files_router)

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


