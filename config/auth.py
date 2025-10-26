from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# --- Change is here ---
# Print the hash to see the output
hashed = hash_password("admin")
print(f"Hashed password: {hashed}")

# You can also test the verify function
is_correct = verify_password("admin", hashed)
print(f"Password verified: {is_correct}")