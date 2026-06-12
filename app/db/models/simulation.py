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


class SimulatedTelemetry(Base):
    __tablename__ = "simulated_telemetry"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    device_uid = Column(String(80), nullable=False, index=True)
    device_model = Column(String(80), nullable=False)
    location_label = Column(String(120), nullable=False)
    profile = Column(String(80), nullable=False)

    pm1 = Column(Float, nullable=True)
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    co2 = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    tvoc = Column(Float, nullable=True)
    nox = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulatedDeviceHealth(Base):
    __tablename__ = "simulated_device_health"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    device_uid = Column(String(80), nullable=False, index=True)
    health_score = Column(Float, nullable=False, default=100.0)
    status = Column(String(40), nullable=False, default="healthy")
    message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulatedQraAlignment(Base):
    __tablename__ = "simulated_qra_alignment"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    device_uid = Column(String(80), nullable=False, index=True)
    nearest_qern_station = Column(String(120), nullable=False)
    alignment_score = Column(Float, nullable=False)
    drift_percent = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    recommendation = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulatedWorkOrder(Base):
    __tablename__ = "simulated_work_orders"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    device_uid = Column(String(80), nullable=False, index=True)
    work_order_type = Column(String(80), nullable=False)
    priority = Column(String(40), nullable=False)
    status = Column(String(40), nullable=False, default="open")
    source = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulatedFieldVisit(Base):
    __tablename__ = "simulated_field_visits"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    work_order_id = Column(Integer, nullable=False, index=True)
    device_uid = Column(String(80), nullable=False, index=True)
    technician_team = Column(String(80), nullable=False)
    visit_status = Column(String(40), nullable=False, default="assigned")
    scheduled_window = Column(String(120), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulatedSlaRecord(Base):
    __tablename__ = "simulated_sla_records"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    organization_name = Column(String(160), nullable=False, index=True)
    sla_model = Column(String(80), nullable=False, default="Enterprise SLA")
    open_work_orders = Column(Integer, nullable=False, default=0)
    field_visits = Column(Integer, nullable=False, default=0)
    compliance_status = Column(String(40), nullable=False)
    compliance_score = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulatedInvoice(Base):
    __tablename__ = "simulated_invoices"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    organization_name = Column(String(160), nullable=False, index=True)
    invoice_type = Column(String(80), nullable=False, default="Business Subscription")
    subscription_model = Column(String(120), nullable=False, default="QAIR Enterprise Subscription")
    amount_qAR = Column(Float, nullable=False)
    status = Column(String(40), nullable=False, default="issued")
    billing_note = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SimulatedScenarioInjection(Base):
    __tablename__ = "simulated_scenario_injections"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    scenario_name = Column(String(120), nullable=False)
    severity = Column(String(40), nullable=False, default="moderate")
    affected_scope = Column(String(120), nullable=False, default="school_network")
    effect_summary = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
