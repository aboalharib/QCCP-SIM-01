from sqlalchemy import func

from app.db.database import SessionLocal
from app.db.models.simulation import SimulatedOrganization, SimulatedDevice, SimulatedInvoice


BASE_SUBSCRIPTION_QAR = 1500.0
DEVICE_SUBSCRIPTION_QAR = 350.0
SUPPORT_SLA_QAR = 500.0


def generate_billing(batch_id: int):
    db = SessionLocal()

    existing = db.query(SimulatedInvoice).filter(
        SimulatedInvoice.batch_id == batch_id
    ).count()

    if existing > 0:
        db.close()
        return {
            "batch_id": batch_id,
            "created": False,
            "message": "Invoices already generated",
            "invoices": existing,
        }

    schools = db.query(SimulatedOrganization).filter(
        SimulatedOrganization.batch_id == batch_id,
        SimulatedOrganization.account_type == "Business",
        SimulatedOrganization.billing_enabled == "yes",
    ).all()

    created = 0

    for school in schools:
        device_count = db.query(SimulatedDevice).filter(
            SimulatedDevice.batch_id == batch_id,
            SimulatedDevice.organization_name == school.organization_name,
        ).count()

        amount = BASE_SUBSCRIPTION_QAR + (device_count * DEVICE_SUBSCRIPTION_QAR) + SUPPORT_SLA_QAR

        db.add(
            SimulatedInvoice(
                batch_id=batch_id,
                organization_name=school.organization_name,
                invoice_type="Business Subscription",
                subscription_model="QAIR Enterprise Subscription",
                amount_qAR=amount,
                status="issued",
                billing_note="MOEHE oversight only. Invoice belongs to school business account.",
            )
        )

        created += 1

    db.commit()
    db.close()

    return {
        "batch_id": batch_id,
        "created": True,
        "invoices_created": created,
    }


def billing_summary(batch_id: int):
    db = SessionLocal()

    invoice_count = db.query(SimulatedInvoice).filter(
        SimulatedInvoice.batch_id == batch_id
    ).count()

    total_amount = db.query(func.sum(SimulatedInvoice.amount_qAR)).filter(
        SimulatedInvoice.batch_id == batch_id
    ).scalar()

    issued = db.query(SimulatedInvoice).filter(
        SimulatedInvoice.batch_id == batch_id,
        SimulatedInvoice.status == "issued",
    ).count()

    db.close()

    return {
        "batch_id": batch_id,
        "invoices": invoice_count,
        "issued": issued,
        "total_amount_qAR": round(total_amount or 0, 2),
        "moehe_billing": "none",
    }
