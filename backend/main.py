import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="ABC Sports Centre Activities API")

# Production-ready CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class Registration(BaseModel):
    email: str
    team: str

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

enrollments = []

@app.get("/")
def read_root():
    return {"message": "ABC Sports Centre Activities API", "status": "healthy"}

@app.get("/activities")
def get_activities():
    return {"activities": ACTIVITIES, "featured": FEATURED_ACTIVITIES}

@app.post("/enroll")
def enroll_activity(reg: Registration):
    if reg.team not in ACTIVITIES:
        raise HTTPException(status_code=400, detail="Invalid activity selected.")
    enrollments.append({"email": reg.email, "activity": reg.team})
    return {"message": f"Enrolled in {reg.team} at ABC Sports Centre!"}
