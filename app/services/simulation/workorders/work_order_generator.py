from sqlalchemy import func

from app.db.database import SessionLocal
from app.db.models.simulation import (
    SimulatedQraAlignment,
    SimulatedWorkOrder,
)


def generate_work_orders(batch_id: int):
    db = SessionLocal()

    existing = (
        db.query(SimulatedWorkOrder)
        .filter(SimulatedWorkOrder.batch_id == batch_id)
        .count()
    )

    if existing > 0:
        db.close()
        return {
            "batch_id": batch_id,
            "created": False,
            "message": "Work orders already generated for this batch",
            "work_orders": existing,
        }

    alignments = (
        db.query(SimulatedQraAlignment)
        .filter(SimulatedQraAlignment.batch_id == batch_id)
        .all()
    )

    created = 0

    for alignment in alignments:
        if alignment.drift_percent >= 10:
            work_order_type = "Drift Investigation"
            priority = "High"
        elif alignment.drift_percent >= 7:
            work_order_type = "Calibration"
            priority = "Medium"
        elif alignment.drift_percent >= 5:
            work_order_type = "Data Quality Review"
            priority = "Low"
        else:
            continue

        db.add(
            SimulatedWorkOrder(
                batch_id=batch_id,
                device_uid=alignment.device_uid,
                work_order_type=work_order_type,
                priority=priority,
                status="open",
                source="QRA",
                description=(
                    f"{work_order_type} required for {alignment.device_uid}. "
                    f"Drift={alignment.drift_percent}%, "
                    f"alignment={alignment.alignment_score}%."
                ),
            )
        )

        created += 1

    db.commit()
    db.close()

    return {
        "batch_id": batch_id,
        "created": True,
        "work_orders_created": created,
    }


def work_order_summary(batch_id: int):
    db = SessionLocal()

    total = (
        db.query(SimulatedWorkOrder)
        .filter(SimulatedWorkOrder.batch_id == batch_id)
        .count()
    )

    open_count = (
        db.query(SimulatedWorkOrder)
        .filter(
            SimulatedWorkOrder.batch_id == batch_id,
            SimulatedWorkOrder.status == "open",
        )
        .count()
    )

    high = (
        db.query(SimulatedWorkOrder)
        .filter(
            SimulatedWorkOrder.batch_id == batch_id,
            SimulatedWorkOrder.priority == "High",
        )
        .count()
    )

    medium = (
        db.query(SimulatedWorkOrder)
        .filter(
            SimulatedWorkOrder.batch_id == batch_id,
            SimulatedWorkOrder.priority == "Medium",
        )
        .count()
    )

    low = (
        db.query(SimulatedWorkOrder)
        .filter(
            SimulatedWorkOrder.batch_id == batch_id,
            SimulatedWorkOrder.priority == "Low",
        )
        .count()
    )

    db.close()

    return {
        "batch_id": batch_id,
        "total_work_orders": total,
        "open_work_orders": open_count,
        "high_priority": high,
        "medium_priority": medium,
        "low_priority": low,
    }
