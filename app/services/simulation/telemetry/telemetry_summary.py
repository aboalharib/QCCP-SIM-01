from sqlalchemy import func

from app.db.database import SessionLocal
from app.db.models.simulation import (
    SimulatedTelemetry,
    SimulatedDeviceHealth,
)


def telemetry_summary(batch_id: int):
    db = SessionLocal()

    telemetry_count = (
        db.query(SimulatedTelemetry)
        .filter(SimulatedTelemetry.batch_id == batch_id)
        .count()
    )

    health_count = (
        db.query(SimulatedDeviceHealth)
        .filter(SimulatedDeviceHealth.batch_id == batch_id)
        .count()
    )

    avg_pm25 = (
        db.query(func.avg(SimulatedTelemetry.pm25))
        .filter(SimulatedTelemetry.batch_id == batch_id)
        .scalar()
    )

    avg_pm10 = (
        db.query(func.avg(SimulatedTelemetry.pm10))
        .filter(SimulatedTelemetry.batch_id == batch_id)
        .scalar()
    )

    avg_co2 = (
        db.query(func.avg(SimulatedTelemetry.co2))
        .filter(SimulatedTelemetry.batch_id == batch_id)
        .scalar()
    )

    healthy = (
        db.query(SimulatedDeviceHealth)
        .filter(
            SimulatedDeviceHealth.batch_id == batch_id,
            SimulatedDeviceHealth.status == "healthy",
        )
        .count()
    )

    warning = (
        db.query(SimulatedDeviceHealth)
        .filter(
            SimulatedDeviceHealth.batch_id == batch_id,
            SimulatedDeviceHealth.status == "warning",
        )
        .count()
    )

    critical = (
        db.query(SimulatedDeviceHealth)
        .filter(
            SimulatedDeviceHealth.batch_id == batch_id,
            SimulatedDeviceHealth.status == "critical",
        )
        .count()
    )

    db.close()

    return {
        "batch_id": batch_id,
        "telemetry_samples": telemetry_count,
        "health_records": health_count,
        "average_pm25": round(avg_pm25 or 0, 2),
        "average_pm10": round(avg_pm10 or 0, 2),
        "average_co2": round(avg_co2 or 0, 2),
        "healthy_devices": healthy,
        "warning_devices": warning,
        "critical_devices": critical,
    }
