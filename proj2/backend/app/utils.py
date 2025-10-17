import secrets
from pydantic import SecretStr
import hashlib
from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _unwrap_secret(password):
    # Works whether it's a Pydantic SecretStr or a normal string
    if isinstance(password, SecretStr):
        return password.get_secret_value()
    return password


def hash_password(password):
    password = _unwrap_secret(password)
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""

    print("verify_password types:", type(plain_password), type(hashed_password))
    print("hashed_password repr:", repr(hashed_password))
    return pwd_context.verify(plain_password, hashed_password)


def generate_verification_token() -> str:
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)


def create_verification_token_hash(email: str, token: str) -> str:
    """Create a hash of email + token for verification"""
    return hashlib.sha256(f"{email}{token}".encode()).hexdigest()


def send_verification_email(email: str, token: str, user_type: str = "user"):
    """Send (or simulate sending) verification email"""
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    verification_link = f"{BASE_URL}/api/auth/verify?email={email}&token={token}&type={user_type}"

    # For testing, just print the link
    print(f"✅ Verification link for {email}: {verification_link}")
    return True
