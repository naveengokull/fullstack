from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "sqlite:///./assessment.db"

if os.path.exists("assessment.db"):
    try:
        import sqlite3
        conn = sqlite3.connect("assessment.db")
        conn.execute("PRAGMA integrity_check")
        conn.close()
    except sqlite3.DatabaseError:
        try:
            os.remove("assessment.db")
            for journal_file in ["assessment.db-journal", "assessment.db-wal", "assessment.db-shm"]:
                if os.path.exists(journal_file):
                    os.remove(journal_file)
        except:
            pass

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

