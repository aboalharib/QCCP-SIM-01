import random

from sqlalchemy import func

from app.db.database import SessionLocal
from app.db.models.simulation import SimulatedDevice, SimulatedQraAlignment


QERN_STATIONS = [
    "Doha QERN Station",
    "Al Rayyan QERN Station",
    "Lusail QERN Station",
    "Al Khor QERN Station",
    "Al Wakrah QERN Station",
    "Umm Salal QERN Station",
]


def run_qra_alignment(batch_id: int):
    db = SessionLocal()

    devices = (
        db.query(SimulatedDevice)
        .filter(SimulatedDevice.batch_id == batch_id)
        .all()
    )

    existing = (
        db.query(SimulatedQraAlignment)
        .filter(SimulatedQraAlignment.batch_id == batch_id)
        .count()
    )

    if existing > 0:
        db.close()
        return {
            "batch_id": batch_id,
            "created": False,
            "message": "QRA alignment already exists for this batch",
            "alignments": existing,
        }

    count = 0

    for device in devices:
        drift = round(random.uniform(1.5, 14.5), 2)
        alignment_score = round(100 - drift, 2)
        confidence = round(random.uniform(82, 98), 2)

        if drift <= 5:
            recommendation = "Aligned with nearest QERN station"
        elif drift <= 10:
            recommendation = "Monitor for moderate drift"
        else:
            recommendation = "Create drift investigation work order"

        db.add(
            SimulatedQraAlignment(
                batch_id=batch_id,
                device_uid=device.device_uid,
                nearest_qern_station=random.choice(QERN_STATIONS),
                alignment_score=alignment_score,
                drift_percent=drift,
                confidence_score=confidence,
                recommendation=recommendation,
            )
        )

        count += 1

    db.commit()
    db.close()

    return {
        "batch_id": batch_id,
        "created": True,
        "alignments": count,
    }


def qra_summary(batch_id: int):
    db = SessionLocal()

    total = (
        db.query(SimulatedQraAlignment)
        .filter(SimulatedQraAlignment.batch_id == batch_id)
        .count()
    )

    avg_alignment = (
        db.query(func.avg(SimulatedQraAlignment.alignment_score))
        .filter(SimulatedQraAlignment.batch_id == batch_id)
        .scalar()
    )

    avg_drift = (
        db.query(func.avg(SimulatedQraAlignment.drift_percent))
        .filter(SimulatedQraAlignment.batch_id == batch_id)
        .scalar()
    )

    avg_confidence = (
        db.query(func.avg(SimulatedQraAlignment.confidence_score))
        .filter(SimulatedQraAlignment.batch_id == batch_id)
        .scalar()
    )

    investigations = (
        db.query(SimulatedQraAlignment)
        .filter(
            SimulatedQraAlignment.batch_id == batch_id,
            SimulatedQraAlignment.recommendation == "Create drift investigation work order",
        )
        .count()
    )

    db.close()

    return {
        "batch_id": batch_id,
        "alignments": total,
        "average_alignment_score": round(avg_alignment or 0, 2),
        "average_drift_percent": round(avg_drift or 0, 2),
        "average_confidence_score": round(avg_confidence or 0, 2),
        "drift_investigations_recommended": investigations,
    }
