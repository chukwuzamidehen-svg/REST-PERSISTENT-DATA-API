from pydantic import BaseModel, Field
import datetime


class ClinicalDataCreate(BaseModel):
    patient_name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=120)
    diagnosis: str = Field(..., min_length=1)

    # Three additional clinical fields
    blood_pressure: str = Field(..., pattern=r"^\d{2,3}/\d{2,3}$", examples=["120/80"])
    heart_rate: int = Field(..., ge=20, le=250)
    body_temperature: float = Field(..., ge=90, le=110)


class ClinicalDataRead(ClinicalDataCreate):
    id: int
    recorded_at: datetime.datetime
