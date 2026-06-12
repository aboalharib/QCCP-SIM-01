import random

from app.db.database import SessionLocal
from app.db.models.simulation import (
    SimulatedDevice,
    SimulatedTelemetry,
    SimulatedDeviceHealth,
)


def generate_value(low: float, high: float) -> float:
    return round(random.uniform(low, high), 2)


def send_telemetry_batch(batch_id: int, profile: str = "normal_school_day"):
    db = SessionLocal()

    devices = (
        db.query(SimulatedDevice)
        .filter(SimulatedDevice.batch_id == batch_id)
        .all()
    )

    telemetry_count = 0
    health_count = 0

    for device in devices:
        if device.device_model == "TA100-IN":
            telemetry = SimulatedTelemetry(
                batch_id=batch_id,
                device_uid=device.device_uid,
                device_model=device.device_model,
                location_label=device.location_label,
                profile=profile,
                pm1=generate_value(5, 20),
                pm25=generate_value(15, 45),
                pm10=generate_value(20, 70),
                co2=generate_value(500, 1600),
                temperature=generate_value(22, 28),
                humidity=generate_value(35, 65),
                tvoc=generate_value(50, 450),
                nox=generate_value(1, 25),
            )
        else:
            if device.location_label == "Main Gate":
                pm25_min, pm25_max = 25, 70
                pm10_min, pm10_max = 40, 130
            else:
                pm25_min, pm25_max = 20, 60
                pm10_min, pm10_max = 35, 120

            telemetry = SimulatedTelemetry(
                batch_id=batch_id,
                device_uid=device.device_uid,
                device_model=device.device_model,
                location_label=device.location_label,
                profile=profile,
                pm25=generate_value(pm25_min, pm25_max),
                pm10=generate_value(pm10_min, pm10_max),
                temperature=generate_value(28, 44),
                humidity=generate_value(25, 70),
            )

        health_score = 100.0
        status = "healthy"
        message = "Telemetry received"

        health = SimulatedDeviceHealth(
            batch_id=batch_id,
            device_uid=device.device_uid,
            health_score=health_score,
            status=status,
            message=message,
        )

        db.add(telemetry)
        db.add(health)

        telemetry_count += 1
        health_count += 1

    db.commit()
    db.close()

    return {
        "batch_id": batch_id,
        "profile": profile,
        "devices_processed": len(devices),
        "telemetry_samples_created": telemetry_count,
        "health_records_created": health_count,
    }
