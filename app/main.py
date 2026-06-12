from fastapi import FastAPI

from app.api.simulation import router as simulation_router
from app.db.database import engine
from app.db.models.simulation import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="QCCP School Simulator",
    version="1.0.0",
)

app.include_router(simulation_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "qccp-school-simulator",
        "database": "ready",
    }
