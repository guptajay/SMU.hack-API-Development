"""
Introduction to API Development
SMU .hack 2024
"""

# Imports
import uvicorn
from fastapi import FastAPI, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from database import SessionLocal
from schema import DBMember
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

# Create a FastAPI Instance
app = FastAPI()

# Database Dependency
# Create a session for a request. 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# A Pydantic Member
# Data validation and settings management using python type annotations.
class Member(BaseModel):
    name: str
    school: str
    graduation_year: int
    
    # Allow ORM fetch
    class Config:
        from_attributes = True

# Methods for interacting with the SQLite Database
# ------------------------------------------------
def get_member(db: Session, member_id: int):
    return db.query(DBMember).where(DBMember.id == member_id).first()

def get_members(db: Session, sort_by: str):
    if(sort_by == 'desc'):
        return db.query(DBMember).order_by(desc(DBMember.name)).all()
    elif(sort_by == 'asc'):
        return db.query(DBMember).order_by(asc(DBMember.name)).all()
    else:
        return db.query(DBMember).all()

def create_member(db: Session, member: Member):
    db_member = DBMember(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member
# ------------------------------------------------


# API Routes
# ------------------------------------------------
@app.post('/members/', response_model=Member)
def create_members_view(member: Member, db: Session = Depends(get_db)):
    db_member = create_member(db, member)
    return db_member

@app.get('/members/', response_model=List[Member])
def get_members_view(db: Session = Depends(get_db), sort_by: Optional[str] = None):
    return get_members(db, sort_by)

@app.get('/member/{member_id}')
def get_member_view(member_id: int, db: Session = Depends(get_db)):
    return get_member(db, member_id)
# ------------------------------------------------

# Health Check
@app.get('/healthcheck', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    return {'healthcheck': 'Everything OK!'}