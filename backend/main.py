from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, Dict, List

app = FastAPI(title="ABC Sports Centre Activities API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Registration(BaseModel):
    email: str
    team: str

class AttendanceUpdate(BaseModel):
    enrollment_id: int
    attendance_status: str  # "present", "absent", or "not_set"

ACTIVITIES = [
    "Basketball",
    "Soccer",
    "Yoga",
    "Swimming",
    "Badminton",
    "Table Tennis",
    "Zumba",
    "Martial Arts",
]

FEATURED_ACTIVITIES = [
    "Basketball",
    "Yoga",
    "Swimming",
]

# Enhanced enrollments list with more detailed structure
enrollments = []
enrollment_counter = 1

# Add some sample data for demonstration
def initialize_sample_data():
    global enrollment_counter
    from datetime import timedelta
    
    sample_enrollments = [
        {"email": "john@example.com", "activity": "Basketball", "days_ago": 2, "status": "present"},
        {"email": "jane@example.com", "activity": "Yoga", "days_ago": 2, "status": "present"},
        {"email": "bob@example.com", "activity": "Swimming", "days_ago": 2, "status": "absent"},
        {"email": "alice@example.com", "activity": "Basketball", "days_ago": 1, "status": "present"},
        {"email": "charlie@example.com", "activity": "Soccer", "days_ago": 1, "status": "not_set"},
        {"email": "diana@example.com", "activity": "Yoga", "days_ago": 0, "status": "not_set"},
        {"email": "eve@example.com", "activity": "Swimming", "days_ago": 0, "status": "not_set"},
    ]
    
    for sample in sample_enrollments:
        enrollment_date = (date.today() - timedelta(days=sample["days_ago"])).isoformat()
        enrollment = {
            "id": enrollment_counter,
            "email": sample["email"],
            "activity": sample["activity"],
            "enrollment_date": enrollment_date,
            "attendance_status": sample["status"]
        }
        enrollments.append(enrollment)
        enrollment_counter += 1

# Initialize sample data
initialize_sample_data()

@app.get("/activities")
def get_activities():
    return {"activities": ACTIVITIES, "featured": FEATURED_ACTIVITIES}

@app.post("/enroll")
def enroll_activity(reg: Registration):
    global enrollment_counter
    if reg.team not in ACTIVITIES:
        raise HTTPException(status_code=400, detail="Invalid activity selected.")
    
    enrollment = {
        "id": enrollment_counter,
        "email": reg.email,
        "activity": reg.team,
        "enrollment_date": date.today().isoformat(),
        "attendance_status": "not_set"
    }
    enrollments.append(enrollment)
    enrollment_counter += 1
    return {"message": f"Enrolled in {reg.team} at ABC Sports Centre!"}

@app.get("/enrollments")
def get_enrollments():
    """Get all enrollments for reporting"""
    return {"enrollments": enrollments}

@app.get("/reports/daily")
def get_daily_reports():
    """Get enrollment counts and attendance by day"""
    daily_stats = {}
    
    for enrollment in enrollments:
        enrollment_date = enrollment["enrollment_date"]
        if enrollment_date not in daily_stats:
            daily_stats[enrollment_date] = {
                "date": enrollment_date,
                "total_enrollments": 0,
                "present": 0,
                "absent": 0,
                "not_set": 0,
                "enrollments": []
            }
        
        daily_stats[enrollment_date]["total_enrollments"] += 1
        daily_stats[enrollment_date]["enrollments"].append(enrollment)
        
        # Count attendance status
        status = enrollment["attendance_status"]
        if status in daily_stats[enrollment_date]:
            daily_stats[enrollment_date][status] += 1
    
    # Convert to list and sort by date
    result = list(daily_stats.values())
    result.sort(key=lambda x: x["date"], reverse=True)
    
    return {"daily_reports": result}

@app.put("/attendance/{enrollment_id}")
def update_attendance(enrollment_id: int, attendance: AttendanceUpdate):
    """Update attendance status for an enrollment"""
    if attendance.attendance_status not in ["present", "absent", "not_set"]:
        raise HTTPException(status_code=400, detail="Invalid attendance status. Must be 'present', 'absent', or 'not_set'")
    
    for enrollment in enrollments:
        if enrollment["id"] == enrollment_id:
            enrollment["attendance_status"] = attendance.attendance_status
            return {"message": f"Attendance updated to {attendance.attendance_status}"}
    
    raise HTTPException(status_code=404, detail="Enrollment not found")
