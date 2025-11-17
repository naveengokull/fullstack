import sys
import os
sys.path.insert(0, '.')

from database import SessionLocal
from models import User
import bcrypt

def reset_admin_password():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == 'admin').first()
        if not user:
            print("Admin user not found. Creating new admin user...")
           
            password_bytes = 'admin123'.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, salt)
            
            user = User(
                username='admin',
                email='admin@example.com',
                hashed_password=hashed.decode('utf-8'),
                full_name='Administrator',
                is_active=1
            )
            db.add(user)
            print("[OK] Admin user created")
        else:
            password_bytes = 'admin123'.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, salt)
            user.hashed_password = hashed.decode('utf-8')
            print("[OK] Admin password reset")
        
        db.commit()
        print("\n[SUCCESS] Admin credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\nYou can now login with these credentials!")
        return True
    except Exception as e:
        db.rollback()
        print(f"[ERROR] {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("  Reset Admin Password")
    print("=" * 50)
    print()
    reset_admin_password()

