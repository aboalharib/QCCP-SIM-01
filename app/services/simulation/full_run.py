from app.services.simulation.service import create_school_network_batch
from app.services.simulation.generators.school_generator import generate_school_network
from app.services.simulation.telemetry.telemetry_generator import send_telemetry_batch
from app.services.simulation.qra.qra_alignment import run_qra_alignment
from app.services.simulation.workorders.work_order_generator import generate_work_orders
from app.services.simulation.workorders.field_service_generator import schedule_field_visits
from app.services.simulation.billing.sla_evaluator import evaluate_sla
from app.services.simulation.billing.billing_generator import generate_billing
from app.services.simulation.service_executive import executive_summary


def run_full_school_network():
    batch = create_school_network_batch()
    batch_id = batch["batch_id"]

    generate_school_network(batch_id)
    send_telemetry_batch(batch_id)
    run_qra_alignment(batch_id)
    generate_work_orders(batch_id)
    schedule_field_visits(batch_id)
    evaluate_sla(batch_id)
    generate_billing(batch_id)

    return executive_summary(batch_id)
