from sqlalchemy import Column, DateTime, Float, Integer, String, Text, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class SimulationBatch(Base):
    __tablename__ = "simulation_batches"

    id = Column(Integer, primary_key=True, index=True)
    batch_name = Column(String(120), nullable=False, unique=True)
    scenario_name = Column(String(120), nullable=False)
    status = Column(String(40), nullable=False, default="created")
    platform_scope = Column(String(40), nullable=False, default="qccp")
    module = Column(String(40), nullable=False, default="qair")
    metadata_json = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SimulationEvent(Base):
    __tablename__ = "simulation_events"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    event_type = Column(String(80), nullable=False)
    entity_type = Column(String(80), nullable=True)
    entity_ref = Column(String(120), nullable=True)
    message = Column(Text, nullable=False)
    payload = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulatedOrganization(Base):
    __tablename__ = "simulated_organizations"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    organization_name = Column(String(160), nullable=False)
    abbreviation = Column(String(40), nullable=True)
    customer_type = Column(String(80), nullable=False)
    account_type = Column(String(80), nullable=False)
    oversight_parent = Column(String(160), nullable=True)
    billing_enabled = Column(String(10), nullable=False, default="yes")

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulatedUser(Base):
    __tablename__ = "simulated_users"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    organization_name = Column(String(160), nullable=False)
    full_name = Column(String(160), nullable=False)
    email = Column(String(160), nullable=False)
    role = Column(String(80), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulatedSite(Base):
    __tablename__ = "simulated_sites"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    organization_name = Column(String(160), nullable=False)
    site_name = Column(String(160), nullable=False)
    site_type = Column(String(80), nullable=False, default="School")
    municipality = Column(String(80), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulatedDevice(Base):
    __tablename__ = "simulated_devices"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    organization_name = Column(String(160), nullable=False)
    site_name = Column(String(160), nullable=False)
    device_uid = Column(String(80), nullable=False, unique=True)
    device_model = Column(String(80), nullable=False)
    location_label = Column(String(120), nullable=False)
    reference_status = Column(String(80), nullable=False, default="non_reference")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
