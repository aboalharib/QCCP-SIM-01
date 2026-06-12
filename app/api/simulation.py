from fastapi import APIRouter

from app.services.simulation.service import create_school_network_batch
from app.services.simulation.generators.school_generator import generate_school_network

router = APIRouter(
    prefix="/api/v1/simulation",
    tags=["simulation"],
)


@router.post("/batches/create-school-network")
def create_batch():
    return create_school_network_batch()


@router.post("/batches/{batch_id}/generate-school-network")
def generate_batch_school_network(batch_id: int):
    return generate_school_network(batch_id)
