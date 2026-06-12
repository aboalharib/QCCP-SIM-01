from fastapi import APIRouter

from app.services.simulation.service import (
    create_school_network_batch,
    get_batch_summary,
)
from app.services.simulation.generators.school_generator import generate_school_network
from app.services.simulation.telemetry.telemetry_generator import send_telemetry_batch
from app.services.simulation.telemetry.telemetry_summary import telemetry_summary
from app.services.simulation.qra.qra_alignment import run_qra_alignment, qra_summary

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


@router.get("/batches/{batch_id}/telemetry/summary")
def get_telemetry_summary(batch_id: int):
    return telemetry_summary(batch_id)


@router.post("/batches/{batch_id}/qra/run")
def run_batch_qra(batch_id: int):
    return run_qra_alignment(batch_id)


@router.get("/batches/{batch_id}/qra/summary")
def get_qra_summary(batch_id: int):
    return qra_summary(batch_id)
