from app.db.database import SessionLocal
from app.db.models.simulation import (
    SimulatedOrganization,
    SimulatedSite,
    SimulatedUser,
    SimulatedDevice,
)


SCHOOLS = [
    "Swiss International School",
    "SEK International School",
    "Doha College",
    "Park House",
    "Hamilton International School",
    "Newton International School",
    "Newton British School",
    "Newton Academy",
    "Newton Lagoon",
    "Qatar Academy Doha",
    "Qatar Academy Al Khor",
    "GEMS Wellington",
    "Compass International",
    "Sherborne Qatar",
    "Durham School",
    "ACS Doha",
    "Al Khor International School",
    "Nord Anglia Al Khor",
    "English Modern School",
    "Choueifat Doha",
]


def safe_slug(name: str) -> str:
    return (
        name.lower()
        .replace("&", "and")
        .replace("'", "")
        .replace(".", "")
        .replace(" ", "_")
    )


def generate_school_network(batch_id: int):
    db = SessionLocal()

    existing_devices = (
        db.query(SimulatedDevice)
        .filter(SimulatedDevice.batch_id == batch_id)
        .count()
    )

    if existing_devices > 0:
        db.close()
        return {
            "generated": False,
            "message": "School network already generated for this batch",
        }

    moehe = SimulatedOrganization(
        batch_id=batch_id,
        organization_name="Ministry of Education and Higher Education",
        abbreviation="MOEHE",
        customer_type="Government",
        account_type="Government",
        oversight_parent=None,
        billing_enabled="no",
    )

    db.add(moehe)

    device_count = 0
    site_count = 0
    user_count = 0

    for index, school in enumerate(SCHOOLS, start=1):
        slug = safe_slug(school)

        org = SimulatedOrganization(
            batch_id=batch_id,
            organization_name=school,
            abbreviation=None,
            customer_type="Education",
            account_type="Business",
            oversight_parent="MOEHE",
            billing_enabled="yes",
        )

        db.add(org)

        site = SimulatedSite(
            batch_id=batch_id,
            organization_name=school,
            site_name=f"{school} Campus",
            municipality="Doha",
            latitude=25.2854 + (index * 0.003),
            longitude=51.5310 + (index * 0.003),
        )

        db.add(site)
        site_count += 1

        roles = [
            "School Admin",
            "Facility Manager",
            "Health Officer",
            "ICT Coordinator",
            "Viewer",
        ]

        for role in roles:
            db.add(
                SimulatedUser(
                    batch_id=batch_id,
                    organization_name=school,
                    full_name=f"{role} - {school}",
                    email=f"{role.lower().replace(' ', '_')}.{slug}@sim.local",
                    role=role,
                )
            )
            user_count += 1

        devices = [
            ("TA100-IN", "Main Building"),
            ("TA200-MG", "Main Gate"),
            ("TA200-PG", "Playground"),
        ]

        for model, location in devices:
            device_count += 1

            db.add(
                SimulatedDevice(
                    batch_id=batch_id,
                    organization_name=school,
                    site_name=f"{school} Campus",
                    device_uid=f"SIM-{index:02d}-{model}",
                    device_model=model,
                    location_label=location,
                )
            )

    db.commit()
    db.close()

    return {
        "generated": True,
        "schools": len(SCHOOLS),
        "government_accounts": 1,
        "business_accounts": len(SCHOOLS),
        "sites": site_count,
        "devices": device_count,
        "users": user_count,
    }
