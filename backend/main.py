from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os

# Database setup
DATABASE_URL = "sqlite:///./activities.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_featured = Column(Integer, default=0)  # 0 = False, 1 = True

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    activity_name = Column(String, index=True)
    enrolled_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ABC Sports Centre Activities API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Registration(BaseModel):
    email: str
    team: str

# Initialize database with activities if empty
def init_db():
    db = SessionLocal()
    try:
        # Check if activities table is empty
        if db.query(Activity).count() == 0:
            # Add initial activities
            activities_data = [
                ("Basketball", True),
                ("Soccer", False),
                ("Yoga", True),
                ("Swimming", True),
                ("Badminton", False),
                ("Table Tennis", False),
                ("Zumba", False),
                ("Martial Arts", False),
            ]
            
            for name, is_featured in activities_data:
                activity = Activity(name=name, is_featured=1 if is_featured else 0)
                db.add(activity)
            
            db.commit()
    finally:
        db.close()

# Initialize database on startup
init_db()

@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    all_activities = db.query(Activity).all()
    activities = [activity.name for activity in all_activities]
    featured = [activity.name for activity in all_activities if activity.is_featured == 1]
    return {"activities": activities, "featured": featured}

@app.post("/enroll")
def enroll_activity(reg: Registration, db: Session = Depends(get_db)):
    # Check if activity exists
    activity = db.query(Activity).filter(Activity.name == reg.team).first()
    if not activity:
        raise HTTPException(status_code=400, detail="Invalid activity selected.")
    
    # Create enrollment
    enrollment = Enrollment(email=reg.email, activity_name=reg.team)
    db.add(enrollment)
    db.commit()
    
    return {"message": f"Enrolled in {reg.team} at ABC Sports Centre!"}

# Optional: Add endpoint to get enrollments (for admin purposes)
@app.get("/enrollments")
def get_enrollments(db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).all()
    return [{"email": e.email, "activity": e.activity_name, "enrolled_at": e.enrolled_at} for e in enrollments]
