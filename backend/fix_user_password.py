import sys
import os
sys.path.insert(0, '.')

from database import SessionLocal
from models import User
import bcrypt

def reset_user_password(username, new_password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"User '{username}' not found!")
            return False
        
        password_bytes = new_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        user.hashed_password = hashed.decode('utf-8')
        
        db.commit()
        print(f"Password reset successfully for user '{username}'")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db.close()

def delete_user(username):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"User '{username}' not found!")
            return False
        
        db.delete(user)
        db.commit()
        print(f"User '{username}' deleted successfully")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db.close()

def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        if not users:
            print("No users found in database")
        else:
            print("\nExisting users:")
            for user in users:
                print(f"  - {user.username} ({user.email})")
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("  User Password Reset Tool")
    print("=" * 50)
    
    list_users()
    
    print("\nOptions:")
    print("1. Reset password for existing user")
    print("2. Delete user")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ")
    
    if choice == "1":
        username = input("Enter username: ")
        new_password = input("Enter new password (min 6 chars): ")
        if len(new_password) < 6:
            print("Password must be at least 6 characters!")
        else:
            reset_user_password(username, new_password)
    elif choice == "2":
        username = input("Enter username to delete: ")
        confirm = input(f"Are you sure you want to delete '{username}'? (yes/no): ")
        if confirm.lower() in ['yes', 'y']:
            delete_user(username)
        else:
            print("Cancelled")
    else:
        print("Exiting...")

