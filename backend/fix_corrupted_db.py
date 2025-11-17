import os
import sys
sys.path.insert(0, '.')

DB_PATH = "assessment.db"
DB_JOURNAL = "assessment.db-journal"
DB_WAL = "assessment.db-wal"

def fix_database():
    print("=" * 50)
    print("  Fix Corrupted Database")
    print("=" * 50)
    print()
    
    deleted = False
    for db_file in [DB_PATH, DB_JOURNAL, DB_WAL]:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"[OK] Deleted {db_file}")
                deleted = True
            except Exception as e:
                print(f"[ERROR] Could not delete {db_file}: {e}")
    
    if not deleted:
        print("[INFO] No database files found to delete")
    
    print("\nRecreating database...")
    try:
        from database import engine, Base
        from models import User, Employee, Task
        
        Base.metadata.create_all(bind=engine)
        print("[OK] Database recreated successfully!")
        
        print("\nCreating admin user...")
        from models import User
        import bcrypt
        
        db = engine.connect()
        password_bytes = 'admin123'.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        from sqlalchemy import text
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO users (username, email, hashed_password, full_name, is_active)
                VALUES ('admin', 'admin@example.com', :password, 'Administrator', 1)
            """), {"password": hashed.decode('utf-8')})
        
        print("[OK] Admin user created!")
        print("\n[SUCCESS] Database fixed!")
        print("\nLogin credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        
    except Exception as e:
        print(f"[ERROR] Failed to recreate database: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    fix_database()

