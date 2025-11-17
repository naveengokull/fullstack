import sys
sys.path.insert(0, '.')

from models import User

print("Testing password hashing...")
test_password = "test123"
hashed = User.get_password_hash(test_password)
print(f"Password hashed successfully: {hashed[:20]}...")

print("\nTesting password verification...")
test_user = User()
test_user.hashed_password = hashed
is_valid = test_user.verify_password(test_password)
print(f"Password verification: {'PASSED' if is_valid else 'FAILED'}")

print("\nAll authentication tests passed!")

