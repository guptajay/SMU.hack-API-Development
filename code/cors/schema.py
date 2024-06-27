# Importing Database
from database import Base, engine
from sqlalchemy import Column, String, Integer

"""
SMU .hack Member Schema

We represent our database members table with a Python class, which inherits from the Base class
This allows SQLAlchemy to detect and map the class to a database table.
"""
class DBMember(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    school = Column(String)
    graduation_year = Column(Integer)

# Create the table
Base.metadata.create_all(bind=engine)