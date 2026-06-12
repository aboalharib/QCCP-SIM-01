from fastapi import APIRouter

from app.services.simulation.service import (
    create_school_network_batch,
    get_batch_summary,
)
from app.services.simulation.generators.school_generator import generate_school_network
from app.services.simulation.telemetry.telemetry_generator import send_telemetry_batch
from app.services.simulation.telemetry.telemetry_summary import telemetry_summary
from app.services.simulation.qra.qra_alignment import run_qra_alignment, qra_summary
from app.services.simulation.workorders.work_order_generator import generate_work_orders, work_order_summary
from app.services.simulation.workorders.field_service_generator import schedule_field_visits, field_service_summary
from app.services.simulation.billing.sla_evaluator import evaluate_sla, sla_summary
from app.services.simulation.billing.billing_generator import generate_billing, billing_summary
from app.services.simulation.service_executive import executive_summary
from app.services.simulation.scenarios.scenario_engine import inject_scenario, scenario_summary

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


@router.post("/batches/{batch_id}/work-orders/generate")
def generate_batch_work_orders(batch_id: int):
    return generate_work_orders(batch_id)


@router.get("/batches/{batch_id}/work-orders/summary")
def get_work_order_summary(batch_id: int):
    return work_order_summary(batch_id)


@router.post("/batches/{batch_id}/field-service/schedule")
def schedule_batch_field_service(batch_id: int):
    return schedule_field_visits(batch_id)


@router.get("/batches/{batch_id}/field-service/summary")
def get_field_service_summary(batch_id: int):
    return field_service_summary(batch_id)


@router.post("/batches/{batch_id}/sla/evaluate")
def evaluate_batch_sla(batch_id: int):
    return evaluate_sla(batch_id)


@router.get("/batches/{batch_id}/sla/summary")
def get_sla_summary(batch_id: int):
    return sla_summary(batch_id)


@router.post("/batches/{batch_id}/billing/generate")
def generate_batch_billing(batch_id: int):
    return generate_billing(batch_id)


@router.get("/batches/{batch_id}/billing/summary")
def get_billing_summary(batch_id: int):
    return billing_summary(batch_id)


@router.get("/batches/{batch_id}/executive/summary")
def get_executive_summary(batch_id: int):
    return executive_summary(batch_id)


@router.post("/batches/{batch_id}/scenarios/inject")
def inject_batch_scenario(batch_id: int, scenario_name: str, severity: str = "moderate"):
    return inject_scenario(batch_id=batch_id, scenario_name=scenario_name, severity=severity)


@router.get("/batches/{batch_id}/scenarios/summary")
def get_scenario_summary(batch_id: int):
    return scenario_summary(batch_id)
