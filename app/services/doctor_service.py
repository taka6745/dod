from sqlalchemy.orm import Session
from app.services.models import Doctor

def add_or_update_doctor(name: str, db: Session):
    doctor = db.query(Doctor).filter(Doctor.name == name).first()
    if not doctor:
        doctor = Doctor(name=name)
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
    return doctor