import os
import sys

DB_PATH = "assessment.db"

def reset_database():
    if os.path.exists(DB_PATH):
        print(f"Deleting existing database: {DB_PATH}")
        os.remove(DB_PATH)
        print("Database deleted")
    else:
        print("Database doesn't exist, will be created")
    
    print("\nRecreating database...")
    from database import engine, Base
    from models import User, Employee, Task
    
    Base.metadata.create_all(bind=engine)
    print("Database recreated successfully!")
    print("\nYou can now create a new account.")
    print("Note: All previous data has been deleted.")

if __name__ == "__main__":
    print("=" * 50)
    print("  Database Reset Tool")
    print("=" * 50)
    print("\n  WARNING: This will delete all data!")
    response = input("\nAre you sure you want to reset the database? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        reset_database()
    else:
        print("\nReset cancelled.")

