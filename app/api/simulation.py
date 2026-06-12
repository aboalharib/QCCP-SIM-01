from fastapi import APIRouter

from app.services.simulation.service import create_school_network_batch, get_batch_summary
from app.services.simulation.generators.school_generator import generate_school_network
from app.services.simulation.telemetry.telemetry_generator import send_telemetry_batch

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


@router.get("/batches/{batch_id}/summary")
def batch_summary(batch_id: int):
    return get_batch_summary(batch_id)


@router.post("/batches/{batch_id}/telemetry/send")
def send_batch_telemetry(batch_id: int, profile: str = "normal_school_day"):
    return send_telemetry_batch(batch_id=batch_id, profile=profile)
