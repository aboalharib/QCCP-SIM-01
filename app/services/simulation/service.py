from app.db.database import SessionLocal
from app.db.models.simulation import SimulationBatch, SimulationEvent


def create_school_network_batch():
    db = SessionLocal()

    batch = SimulationBatch(
        batch_name="school_network_20x3",
        scenario_name="National School Environmental Monitoring",
        status="created",
    )

    db.add(batch)
    db.commit()
    db.refresh(batch)

    event = SimulationEvent(
        batch_id=batch.id,
        event_type="batch_created",
        entity_type="simulation_batch",
        entity_ref=str(batch.id),
        message="School network simulation batch created",
    )

    db.add(event)
    db.commit()

    result = {
        "batch_id": batch.id,
        "batch_name": batch.batch_name,
        "status": batch.status,
    }

    db.close()

    return result
