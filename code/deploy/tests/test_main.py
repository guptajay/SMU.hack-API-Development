from fastapi import Depends
import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, SessionLocal

# Set up a temporary SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite3"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the testing session
@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)  # Ensure the table is created before tests run
    app.dependency_overrides[get_db] = lambda: TestingSessionLocal()
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)  # Clean up the table after tests

def test_healthcheck(client):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"healthcheck": "Everything OK!"}

def test_create_member(client):
    response = client.post("/members/", json={"name": "John Doe", "school": "SMU", "graduation_year": 2024})
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["school"] == "SMU"
    assert response.json()["graduation_year"] == 2024

def test_get_members(client):
    response = client.get("/members/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_members_sorted(client):
    # Test get members sorted by name in ascending order
    response = client.get("/members/?sort_by=asc")
    assert response.status_code == 200
    members = response.json()
    assert all(members[i]["name"] <= members[i + 1]["name"] for i in range(len(members) - 1))

    # Test get members sorted by name in descending order
    response = client.get("/members/?sort_by=desc")
    assert response.status_code == 200
    members = response.json()
    assert all(members[i]["name"] >= members[i + 1]["name"] for i in range(len(members) - 1))