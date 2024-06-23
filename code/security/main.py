"""
Introduction to API Development
SMU .hack 2024

OAuth2.0 Reference: https://fastapi.tiangolo.com/tutorial/security/
"""

# Imports
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from database import SessionLocal
from schema import DBMember
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session


# Create a FastAPI Instance
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


# OAuth2.0
# ------------------------------------------------
fake_users_db = {
    "jaygupta": {
        "username": "jaygupta",
        "full_name": "Jay Gupta",
        "email": "jaygupta@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wondecrson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

def fake_hash_password(password: str):
    return "fakehashed" + password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Get user dictionary from username
    user_dict = fake_users_db.get(form_data.username)
    
    # Check if user exists
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Pass the keys and values of the user_dict
    user = UserInDB(**user_dict)
    
    # Hash the password
    hashed_password = fake_hash_password(form_data.password)
    
    # Check if the password matches
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Return username as access token (simple use case)
    return {"access_token": user.username, "token_type": "bearer"}
# ------------------------------------------------


# API Routes
# ------------------------------------------------
@app.post('/members/', response_model=Member)
def create_members_view(member: Member, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
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