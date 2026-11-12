from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime

from database import Base


class ClinicalData(Base):
    __tablename__ = "clinical_data"

    # Original fields from the professor's example
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    diagnosis = Column(String, nullable=False)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Three additional clinical fields
    blood_pressure = Column(String, nullable=False)
    heart_rate = Column(Integer, nullable=False)
    body_temperature = Column(Float, nullable=False)

    def to_dict(self):
        """Convert a database record into a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "patient_name": self.patient_name,
            "age": self.age,
            "diagnosis": self.diagnosis,
            "blood_pressure": self.blood_pressure,
            "heart_rate": self.heart_rate,
            "body_temperature": self.body_temperature,
            "recorded_at": self.recorded_at.isoformat(),
        }
