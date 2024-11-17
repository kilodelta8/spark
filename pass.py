from passlib.hash import pbkdf2_sha256
import sys

if len(sys.argv) != 2:
    print("Usage: python hash_password.py <password>")
    sys.exit(1)

password = sys.argv[1]
hashed_password = pbkdf2_sha256.hash(password)
print(f"Hashed Password: {hashed_password}")