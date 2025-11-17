import sys
sys.path.insert(0, '.')

from database import SessionLocal
from models import User

def test_login():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == 'admin').first()
        if not user:
            print("ERROR: Admin user not found!")
            return False
        
        print(f"User found: {user.username}")
        print(f"Email: {user.email}")
        print(f"Password hash: {user.hashed_password[:30]}...")
        
        result = user.verify_password('admin123')
        print(f"Password verification (admin123): {result}")
        
        if result:
            print("\n[SUCCESS] Login should work!")
            return True
        else:
            print("\n[ERROR] Password verification failed!")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_login()

