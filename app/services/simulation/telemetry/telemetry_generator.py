import random

from app.db.database import SessionLocal
from app.db.models.simulation import (
    SimulatedDevice,
    SimulatedTelemetry,
    SimulatedDeviceHealth,
    SimulatedScenarioInjection,
)


def generate_value(low: float, high: float) -> float:
    return round(random.uniform(low, high), 2)


def active_scenarios(db, batch_id: int):
    return [
        item.scenario_name
        for item in db.query(SimulatedScenarioInjection)
        .filter(SimulatedScenarioInjection.batch_id == batch_id)
        .all()
    ]


def send_telemetry_batch(batch_id: int, profile: str = "normal_school_day"):
    db = SessionLocal()

    scenarios = active_scenarios(db, batch_id)

    devices = (
        db.query(SimulatedDevice)
        .filter(SimulatedDevice.batch_id == batch_id)
        .all()
    )

    telemetry_count = 0
    health_count = 0

    for device in devices:
        health_score = 100.0
        status = "healthy"
        message = "Telemetry received"

        if device.device_model == "TA100-IN":
            pm25_low, pm25_high = 15, 45
            pm10_low, pm10_high = 20, 70
            temp_low, temp_high = 22, 28

            if "dust_storm" in scenarios:
                pm25_low, pm25_high = 45, 95
                pm10_low, pm10_high = 90, 180

            if "heat_wave" in scenarios:
                temp_low, temp_high = 27, 34

            telemetry = SimulatedTelemetry(
                batch_id=batch_id,
                device_uid=device.device_uid,
                device_model=device.device_model,
                location_label=device.location_label,
                profile=profile,
                pm1=generate_value(5, 20),
                pm25=generate_value(pm25_low, pm25_high),
                pm10=generate_value(pm10_low, pm10_high),
                co2=generate_value(500, 1600),
                temperature=generate_value(temp_low, temp_high),
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

            temp_min, temp_max = 28, 44

            if "dust_storm" in scenarios:
                pm25_min += 35
                pm25_max += 65
                pm10_min += 70
                pm10_max += 120
                health_score -= 10
                status = "warning"
                message = "Dust storm impact detected"

            if "heat_wave" in scenarios:
                temp_min, temp_max = 42, 52
                health_score -= 10
                status = "warning"
                message = "Heat wave impact detected"

            if "internet_outage" in scenarios:
                health_score = 45
                status = "critical"
                message = "Connectivity outage simulated"

            if "sensor_failure" in scenarios:
                health_score = 35
                status = "critical"
                message = "Sensor failure simulated"

            telemetry = SimulatedTelemetry(
                batch_id=batch_id,
                device_uid=device.device_uid,
                device_model=device.device_model,
                location_label=device.location_label,
                profile=profile,
                pm25=generate_value(pm25_min, pm25_max),
                pm10=generate_value(pm10_min, pm10_max),
                temperature=generate_value(temp_min, temp_max),
                humidity=generate_value(25, 70),
            )

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
        "active_scenarios": scenarios,
        "devices_processed": len(devices),
        "telemetry_samples_created": telemetry_count,
        "health_records_created": health_count,
    }
