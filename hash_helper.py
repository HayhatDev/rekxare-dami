import streamlit_authenticator as stauth
import sys

if len(sys.argv) < 2:
    print("Usage: python3 hash_helper.py <password>")
    sys.exit(1)

password = sys.argv[1]
hashed = stauth.Hasher.hash(password)
print(f"Password: {password}")
print(f"Hashed: {hashed}")
