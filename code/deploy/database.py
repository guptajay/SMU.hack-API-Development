from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database Setup
SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///./db.sqlite3:'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# Initialize Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Construct Base Class
Base = declarative_base()