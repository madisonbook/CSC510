import secrets
from pydantic import SecretStr
import hashlib
from datetime import datetime, timedelta
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# fix password encryption after testing
DEV_PLAINTEXT = os.getenv("DEV_PLAINTEXT_PASSWORDS", "0") == "1"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _unwrap_secret(password):
    if isinstance(password, SecretStr):
        return password.get_secret_value()
    return password

def hash_password(password):
    password = _unwrap_secret(password)
    if DEV_PLAINTEXT:
        # In dev mode, return the raw password so it gets stored plaintext (NOT for prod)
        return password
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain = _unwrap_secret(plain_password)

    print("verify_password types:", type(plain), type(hashed_password))
    print("hashed_password repr:", repr(hashed_password))

    if DEV_PLAINTEXT and isinstance(hashed_password, str) and not hashed_password.startswith("$2"):
        return plain == hashed_password

    try:
        return pwd_context.verify(plain, hashed_password)
    except ValueError:
        if DEV_PLAINTEXT:
            return plain == hashed_password
        raise

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
    
    print(f"✅ Verification link for {email}: {verification_link}")
    return True