from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

@app.get("/activities")
def get_activities():
    return {"activities": ACTIVITIES, "featured": FEATURED_ACTIVITIES}

@app.post("/enroll")
def enroll_activity(reg: Registration):
    if reg.team not in ACTIVITIES:
        raise HTTPException(status_code=400, detail="Invalid activity selected.")
    enrollments.append({"email": reg.email, "activity": reg.team})
    return {"message": f"Enrolled in {reg.team} at ABC Sports Centre!"}
