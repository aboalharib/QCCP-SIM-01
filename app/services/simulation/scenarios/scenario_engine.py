from app.db.database import SessionLocal
from app.db.models.simulation import SimulatedScenarioInjection


SUPPORTED_SCENARIOS = {
    "dust_storm": "Increases PM2.5 and PM10 across outdoor devices.",
    "heat_wave": "Increases outdoor temperature and heat exposure risk.",
    "traffic_pollution": "Increases main gate PM2.5 and PM10.",
    "internet_outage": "Simulates connectivity loss for selected devices.",
    "sensor_failure": "Simulates sensor failure and health degradation.",
    "school_closure": "Reduces activity profile across school sites.",
    "national_drill": "Creates national exercise mode for MOEHE oversight.",
}


def inject_scenario(batch_id: int, scenario_name: str, severity: str = "moderate"):
    db = SessionLocal()

    if scenario_name not in SUPPORTED_SCENARIOS:
        db.close()
        return {
            "batch_id": batch_id,
            "accepted": False,
            "message": "Unsupported scenario",
            "supported_scenarios": list(SUPPORTED_SCENARIOS.keys()),
        }

    injection = SimulatedScenarioInjection(
        batch_id=batch_id,
        scenario_name=scenario_name,
        severity=severity,
        affected_scope="school_network",
        effect_summary=SUPPORTED_SCENARIOS[scenario_name],
    )

    db.add(injection)
    db.commit()
    db.refresh(injection)

    result = {
        "batch_id": batch_id,
        "accepted": True,
        "scenario_id": injection.id,
        "scenario_name": scenario_name,
        "severity": severity,
        "effect_summary": injection.effect_summary,
    }

    db.close()
    return result


def scenario_summary(batch_id: int):
    db = SessionLocal()

    scenarios = db.query(SimulatedScenarioInjection).filter(
        SimulatedScenarioInjection.batch_id == batch_id
    ).all()

    result = {
        "batch_id": batch_id,
        "scenario_injections": len(scenarios),
        "scenarios": [
            {
                "scenario_id": scenario.id,
                "scenario_name": scenario.scenario_name,
                "severity": scenario.severity,
                "affected_scope": scenario.affected_scope,
                "effect_summary": scenario.effect_summary,
            }
            for scenario in scenarios
        ],
    }

    db.close()
    return result
