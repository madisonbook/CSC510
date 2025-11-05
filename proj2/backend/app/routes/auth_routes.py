from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from ..models import (
    UserCreate,
    UserLogin,
    UserRole,
    AccountStatus,
    UserStats,
    SocialMediaLinks,
    DietaryPreferences,
)
from app.database import get_database
from ..utils import (
    hash_password,
    verify_password,
)

router = APIRouter()


# User Registration
@router.post(
    "/api/auth/register/user", response_model=dict, status_code=status.HTTP_201_CREATED
)
async def register_user(user: UserCreate):
    """Register a new user account"""
    db = get_database()
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already associated with an account",
        )

    # Hash password
    hashed_password = hash_password(user.password)

    # Create user document - now with ACTIVE status and verified=True
    user_doc = {
        "email": user.email,
        "password": hashed_password,
        "full_name": user.full_name,
        "phone": user.phone,
        "location": user.location.dict(),
        "bio": user.bio,
        "profile_picture": user.profile_picture,
        "dietary_preferences": DietaryPreferences().dict(),
        "social_media": SocialMediaLinks().dict(),
        "role": UserRole.USER,
        "status": AccountStatus.ACTIVE,  # Changed from PENDING to ACTIVE
        "stats": UserStats().dict(),
        "verified": True,  # Changed from False to True
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    # Insert user
    result = await db.users.insert_one(user_doc)

    return {
        "message": "User account created successfully. You can now log in.",
        "user_id": str(result.inserted_id),
        "email": user.email,
    }


# Login
@router.post("/api/auth/login", response_model=dict)
async def login(credentials: UserLogin):
    """Login for users"""
    db = get_database()
    # Check in users collection
    user = await db.users.find_one({"email": credentials.email})
    if user:
        if not verify_password(credentials.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        # Removed email verification check - users can login immediately

        return {
            "message": "Login successful",
            "user_id": str(user["_id"]),
            "email": user["email"],
            "role": user["role"],
            "full_name": user["full_name"],
        }

    # handle user not found
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password"
    )


# End point just for testing
@router.get("/api/debug/users")
async def list_users():
    db = get_database()
    users = await db.users.find().to_list(100)  # limit to 100 users

    for user in users:
        user["_id"] = str(user["_id"])

    return users
