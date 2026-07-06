from fastapi import FastAPI

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