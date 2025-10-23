from passlib.context import CryptContext

# 1. Create a context, specifying 'bcrypt' as the default
# 'deprecated="auto"' means it will auto-upgrade old hashes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")