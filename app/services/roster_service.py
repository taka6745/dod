from sqlalchemy.orm import Session
from app.services.models import Roster, Doctor  # Import Doctor model
from app.services.doctor_service import add_or_update_doctor
from io import StringIO
import csv

def calculate_hours(start_time, end_time):
    bh_start = 8
    bh_end = 18
    start_hour = int(start_time.split(":")[0])
    end_hour = int(end_time.split(":")[0])
    bh = max(0, min(bh_end, end_hour) - max(bh_start, start_hour))
    ah = (end_hour - start_hour) - bh
    return bh, ah

def create_roster(doctor_name: str, date: str, start_time: str, end_time: str, db: Session):
    doctor = add_or_update_doctor(doctor_name, db)
    bh, ah = calculate_hours(start_time, end_time)
    new_roster = Roster(doctor_id=doctor.id, date=date, start_time=start_time, end_time=end_time, business_hours=bh, after_hours=ah)
    db.add(new_roster)
    db.commit()

def export_rosters(start_date: str, end_date: str, db: Session):
    rosters = db.query(Roster).filter(Roster.date.between(start_date, end_date)).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Doctor Name', 'Date', 'Start Time', 'End Time', 'BH', 'AH'])
    
    for roster in rosters:
        doctor = db.query(Doctor).filter(Doctor.id == roster.doctor_id).first()
        writer.writerow([doctor.name, roster.date, roster.start_time, roster.end_time, roster.business_hours, roster.after_hours])
    
    output.seek(0)
    return output.getvalue()
