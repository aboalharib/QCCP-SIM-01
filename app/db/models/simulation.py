from sqlalchemy import Column, DateTime, Integer, String, Text, JSON
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
