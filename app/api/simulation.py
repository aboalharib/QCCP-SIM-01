from fastapi import APIRouter

from app.services.simulation.service import create_school_network_batch

router = APIRouter(
    prefix="/api/v1/simulation",
    tags=["simulation"],
)


@router.post("/batches/create-school-network")
def create_batch():
    return create_school_network_batch()
