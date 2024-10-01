from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.services import doctor_service, roster_service
from app.services.database import get_db
from app.services.models import Doctor, Roster  # Import the Doctor and Roster models
from fastapi.staticfiles import StaticFiles
import io
import csv

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Template rendering
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/doctors/{doctor_id}", response_class=HTMLResponse)
def doctor_form(request: Request, doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return HTMLResponse(content="Doctor not found", status_code=404)
    return templates.TemplateResponse("doctor_form.html", {"request": request, "doctor_id": doctor_id, "doctor_name": doctor.name})

@app.get("/api/rosters/{doctor_id}", response_class=JSONResponse)
def get_rosters(doctor_id: int, db: Session = Depends(get_db)):
    rosters = db.query(Roster).filter(Roster.doctor_id == doctor_id).all()
    events = []
    for roster in rosters:
        events.append({
            'start': roster.date.isoformat(),
            'allDay': True,  # Ensure the event spans the entire day
            'display': 'background',  # Display as background color
            'backgroundColor': '#FFDDC1'  # Pastel yellow
        })
    return JSONResponse(content=events)
@app.delete("/api/rosters/delete/{roster_id}", response_class=JSONResponse)
def delete_roster(roster_id: int, db: Session = Depends(get_db)):
    roster = db.query(Roster).filter(Roster.id == roster_id).first()
    if roster:
        db.delete(roster)
        db.commit()
        return JSONResponse(content={"success": True})
    return JSONResponse(content={"success": False}, status_code=404)
@app.post("/doctors/{doctor_id}", response_class=HTMLResponse)
def submit_roster(request: Request, doctor_id: int, date: str = Form(...), start_time: str = Form(...), end_time: str = Form(...), db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return HTMLResponse(content="Doctor not found", status_code=404)
    roster_service.create_roster(doctor.name, date, start_time, end_time, db)
    return templates.TemplateResponse("doctor_form.html", {"request": request, "doctor_id": doctor_id, "doctor_name": doctor.name, "message": "Roster submitted successfully"})

@app.get("/admin", response_class=HTMLResponse)
def admin_view(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/admin/export", response_class=StreamingResponse)
def export_rosters(request: Request, start_date: str, end_date: str, db: Session = Depends(get_db)):
    csv_data = roster_service.export_rosters(start_date, end_date, db)
    response = StreamingResponse(io.StringIO(csv_data), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=rosters.csv"
    return response

@app.get("/admin/add_doctor", response_class=HTMLResponse)
def admin_add_doctor_form(request: Request):
    return templates.TemplateResponse("admin_add_doctor.html", {"request": request})

@app.post("/admin/add_doctor", response_class=HTMLResponse)
def admin_add_doctor(request: Request, doctor_name: str = Form(...), db: Session = Depends(get_db)):
    doctor_service.add_or_update_doctor(doctor_name, db)
    return templates.TemplateResponse("admin_add_doctor.html", {"request": request, "message": "Doctor added successfully"})

@app.get("/export/doctors", response_class=StreamingResponse)
def export_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Doctor ID', 'Doctor Name'])
    
    for doctor in doctors:
        writer.writerow([doctor.id, doctor.name])
    
    output.seek(0)
    response = StreamingResponse(output, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=doctors.csv"
    return response

@app.delete("/api/rosters/delete/{roster_id}", response_class=JSONResponse)
def delete_roster(roster_id: int, db: Session = Depends(get_db)):
    roster = db.query(Roster).filter(Roster.id == roster_id).first()
    if roster:
        db.delete(roster)
        db.commit()
        return JSONResponse(content={"success": True})
    return JSONResponse(content={"success": False}, status_code=404)

@app.delete("/api/rosters/delete-day/{date}", response_class=JSONResponse)
def delete_day_rosters(date: str, db: Session = Depends(get_db)):
    rosters = db.query(Roster).filter(Roster.date == date).all()
    if rosters:
        for roster in rosters:
            db.delete(roster)
        db.commit()
        return JSONResponse(content={"success": True})
    return JSONResponse(content={"success": False}, status_code=404)