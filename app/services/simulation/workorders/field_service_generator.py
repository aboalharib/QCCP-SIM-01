from app.db.database import SessionLocal
from app.db.models.simulation import SimulatedWorkOrder, SimulatedFieldVisit


TEAMS = ["North Team", "Central Team", "South Team"]


def schedule_field_visits(batch_id: int):
    db = SessionLocal()

    existing = (
        db.query(SimulatedFieldVisit)
        .filter(SimulatedFieldVisit.batch_id == batch_id)
        .count()
    )

    if existing > 0:
        db.close()
        return {
            "batch_id": batch_id,
            "created": False,
            "message": "Field visits already scheduled",
            "field_visits": existing,
        }

    work_orders = (
        db.query(SimulatedWorkOrder)
        .filter(
            SimulatedWorkOrder.batch_id == batch_id,
            SimulatedWorkOrder.status == "open",
        )
        .all()
    )

    created = 0

    for index, work_order in enumerate(work_orders):
        team = TEAMS[index % len(TEAMS)]

        db.add(
            SimulatedFieldVisit(
                batch_id=batch_id,
                work_order_id=work_order.id,
                device_uid=work_order.device_uid,
                technician_team=team,
                visit_status="scheduled",
                scheduled_window="Next 48 hours",
            )
        )

        created += 1

    db.commit()
    db.close()

    return {
        "batch_id": batch_id,
        "created": True,
        "field_visits_scheduled": created,
    }


def field_service_summary(batch_id: int):
    db = SessionLocal()

    total = (
        db.query(SimulatedFieldVisit)
        .filter(SimulatedFieldVisit.batch_id == batch_id)
        .count()
    )

    north = (
        db.query(SimulatedFieldVisit)
        .filter(
            SimulatedFieldVisit.batch_id == batch_id,
            SimulatedFieldVisit.technician_team == "North Team",
        )
        .count()
    )

    central = (
        db.query(SimulatedFieldVisit)
        .filter(
            SimulatedFieldVisit.batch_id == batch_id,
            SimulatedFieldVisit.technician_team == "Central Team",
        )
        .count()
    )

    south = (
        db.query(SimulatedFieldVisit)
        .filter(
            SimulatedFieldVisit.batch_id == batch_id,
            SimulatedFieldVisit.technician_team == "South Team",
        )
        .count()
    )

    scheduled = (
        db.query(SimulatedFieldVisit)
        .filter(
            SimulatedFieldVisit.batch_id == batch_id,
            SimulatedFieldVisit.visit_status == "scheduled",
        )
        .count()
    )

    db.close()

    return {
        "batch_id": batch_id,
        "total_field_visits": total,
        "scheduled": scheduled,
        "north_team": north,
        "central_team": central,
        "south_team": south,
    }
