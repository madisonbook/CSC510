import secrets
import hashlib
from datetime import datetime, timedelta
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def generate_verification_token() -> str:
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

def create_verification_token_hash(email: str, token: str) -> str:
    """Create a hash of email + token for verification"""
    return hashlib.sha256(f"{email}{token}".encode()).hexdigest()

def send_verification_email(email: str, token: str, user_type: str = "user"):
    """Send verification email to user"""
    
    # Configure these with your email service credentials
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@forkcast.com")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your-password")
    
    # Create verification link
    BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")
    verification_link = f"{BASE_URL}/verify?email={email}&token={token}&type={user_type}"
    
    # Create email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Verify Your Forkcast Account"
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    
    # Email body
    text = f"""
    Welcome to Forkcast!
    
    Please verify your email address by clicking the link below:
    {verification_link}
    
    This link will expire in 24 hours.
    
    If you didn't create an account, please ignore this email.
    """
    
    html = f"""
    <html>
      <body>
        <h2>Welcome to Forkcast!</h2>
        <p>Please verify your email address by clicking the button below:</p>
        <a href="{verification_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
          Verify Email
        </a>
        <p>Or copy and paste this link into your browser:</p>
        <p>{verification_link}</p>
        <p>This link will expire in 24 hours.</p>
        <p>If you didn't create an account, please ignore this email.</p>
      </body>
    </html>
    """
    
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    
    # Send email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
