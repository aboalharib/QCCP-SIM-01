from sqlalchemy import func

from app.db.database import SessionLocal
from app.db.models.simulation import (
    SimulatedOrganization,
    SimulatedSite,
    SimulatedUser,
    SimulatedDevice,
    SimulatedTelemetry,
    SimulatedDeviceHealth,
    SimulatedQraAlignment,
    SimulatedWorkOrder,
    SimulatedFieldVisit,
    SimulatedSlaRecord,
    SimulatedInvoice,
)


def executive_summary(batch_id: int):
    db = SessionLocal()

    total_billing = db.query(func.sum(SimulatedInvoice.amount_qAR)).filter(
        SimulatedInvoice.batch_id == batch_id
    ).scalar()

    summary = {
        "batch_id": batch_id,
        "oversight_account": "MOEHE",
        "government_accounts": db.query(SimulatedOrganization).filter(
            SimulatedOrganization.batch_id == batch_id,
            SimulatedOrganization.account_type == "Government",
        ).count(),
        "school_business_accounts": db.query(SimulatedOrganization).filter(
            SimulatedOrganization.batch_id == batch_id,
            SimulatedOrganization.account_type == "Business",
        ).count(),
        "sites": db.query(SimulatedSite).filter(
            SimulatedSite.batch_id == batch_id
        ).count(),
        "devices": db.query(SimulatedDevice).filter(
            SimulatedDevice.batch_id == batch_id
        ).count(),
        "users": db.query(SimulatedUser).filter(
            SimulatedUser.batch_id == batch_id
        ).count(),
        "telemetry_samples": db.query(SimulatedTelemetry).filter(
            SimulatedTelemetry.batch_id == batch_id
        ).count(),
        "health_records": db.query(SimulatedDeviceHealth).filter(
            SimulatedDeviceHealth.batch_id == batch_id
        ).count(),
        "qra_alignments": db.query(SimulatedQraAlignment).filter(
            SimulatedQraAlignment.batch_id == batch_id
        ).count(),
        "open_work_orders": db.query(SimulatedWorkOrder).filter(
            SimulatedWorkOrder.batch_id == batch_id,
            SimulatedWorkOrder.status == "open",
        ).count(),
        "field_visits": db.query(SimulatedFieldVisit).filter(
            SimulatedFieldVisit.batch_id == batch_id
        ).count(),
        "sla_records": db.query(SimulatedSlaRecord).filter(
            SimulatedSlaRecord.batch_id == batch_id
        ).count(),
        "invoices": db.query(SimulatedInvoice).filter(
            SimulatedInvoice.batch_id == batch_id
        ).count(),
        "total_billing_qAR": round(total_billing or 0, 2),
        "moehe_billing": "none",
    }

    db.close()
    return summary
