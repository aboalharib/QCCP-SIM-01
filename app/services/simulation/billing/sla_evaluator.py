from app.db.database import SessionLocal
from app.db.models.simulation import (
    SimulatedOrganization,
    SimulatedWorkOrder,
    SimulatedFieldVisit,
    SimulatedDevice,
    SimulatedSlaRecord,
)


def evaluate_sla(batch_id: int):
    db = SessionLocal()

    existing = db.query(SimulatedSlaRecord).filter(
        SimulatedSlaRecord.batch_id == batch_id
    ).count()

    if existing > 0:
        db.close()
        return {
            "batch_id": batch_id,
            "created": False,
            "message": "SLA already evaluated",
            "sla_records": existing,
        }

    schools = db.query(SimulatedOrganization).filter(
        SimulatedOrganization.batch_id == batch_id,
        SimulatedOrganization.account_type == "Business",
    ).all()

    created = 0

    for school in schools:
        devices = db.query(SimulatedDevice).filter(
            SimulatedDevice.batch_id == batch_id,
            SimulatedDevice.organization_name == school.organization_name,
        ).all()

        device_uids = [d.device_uid for d in devices]

        open_work_orders = db.query(SimulatedWorkOrder).filter(
            SimulatedWorkOrder.batch_id == batch_id,
            SimulatedWorkOrder.device_uid.in_(device_uids),
            SimulatedWorkOrder.status == "open",
        ).count()

        field_visits = db.query(SimulatedFieldVisit).filter(
            SimulatedFieldVisit.batch_id == batch_id,
            SimulatedFieldVisit.device_uid.in_(device_uids),
        ).count()

        score = max(60, 100 - (open_work_orders * 5))

        if score >= 90:
            status = "Compliant"
        elif score >= 75:
            status = "At Risk"
        else:
            status = "Breached"

        db.add(
            SimulatedSlaRecord(
                batch_id=batch_id,
                organization_name=school.organization_name,
                sla_model="Enterprise SLA",
                open_work_orders=open_work_orders,
                field_visits=field_visits,
                compliance_status=status,
                compliance_score=score,
            )
        )

        created += 1

    db.commit()
    db.close()

    return {
        "batch_id": batch_id,
        "created": True,
        "sla_records_created": created,
    }


def sla_summary(batch_id: int):
    db = SessionLocal()

    total = db.query(SimulatedSlaRecord).filter(
        SimulatedSlaRecord.batch_id == batch_id
    ).count()

    compliant = db.query(SimulatedSlaRecord).filter(
        SimulatedSlaRecord.batch_id == batch_id,
        SimulatedSlaRecord.compliance_status == "Compliant",
    ).count()

    at_risk = db.query(SimulatedSlaRecord).filter(
        SimulatedSlaRecord.batch_id == batch_id,
        SimulatedSlaRecord.compliance_status == "At Risk",
    ).count()

    breached = db.query(SimulatedSlaRecord).filter(
        SimulatedSlaRecord.batch_id == batch_id,
        SimulatedSlaRecord.compliance_status == "Breached",
    ).count()

    db.close()

    return {
        "batch_id": batch_id,
        "sla_records": total,
        "compliant": compliant,
        "at_risk": at_risk,
        "breached": breached,
    }
