from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timedelta
from bson import ObjectId


from .models import (
    UserCreate, UserResponse, UserLogin, 
    RestaurantCreate, RestaurantResponse,
    UserRole, AccountStatus, VerificationToken
)
from .database import get_database
from .utils import (
    hash_password, verify_password, 
    generate_verification_token, send_verification_email
)

router = APIRouter()
db = get_database()

# User Registration
@router.post("/api/auth/register/user", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    """Register a new user account"""
    
    # Check if user already exists
    existing_user = db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already associated with an account"
        )
    
    # Hash password
    hashed_password = hash_password(user.password)
    
    # Create user document
    user_doc = {
        "email": user.email,
        "password": hashed_password,
        "full_name": user.full_name,
        "phone": user.phone,
        "address": user.address,
        "role": UserRole.USER,
        "status": AccountStatus.PENDING,
        "preferences": {},
        "allergens": [],
        "verified": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert user
    result = db.users.insert_one(user_doc)
    
    # Generate verification token
    token = generate_verification_token()
    token_doc = {
        "email": user.email,
        "token": token,
        "token_type": "email_verification",
        "expires_at": datetime.utcnow() + timedelta(hours=24),
        "created_at": datetime.utcnow()
    }
    db.verification_tokens.insert_one(token_doc)
    
    # Send verification email
    send_verification_email(user.email, token, "user")
    
    return {
        "message": "User account created successfully. Please check your email to verify your account.",
        "user_id": str(result.inserted_id),
        "email": user.email
    }

# Restaurant Registration
@router.post("/api/auth/register/restaurant", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_restaurant(restaurant: RestaurantCreate):
    """Register a new restaurant account"""
    
    # Check if restaurant already exists
    existing_restaurant = db.restaurants.find_one({"business_email": restaurant.business_email})
    if existing_restaurant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already associated with an account"
        )
    
    # Check for duplicate restaurant name and address
    duplicate_restaurant = db.restaurants.find_one({
        "restaurant_name": restaurant.restaurant_name,
        "address": restaurant.address
    })
    if duplicate_restaurant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This restaurant may already be registered"
        )
    
    # Hash password
    hashed_password = hash_password(restaurant.password)
    
    # Create restaurant document
    restaurant_doc = {
        "business_email": restaurant.business_email,
        "password": hashed_password,
        "restaurant_name": restaurant.restaurant_name,
        "business_registration_number": restaurant.business_registration_number,
        "address": restaurant.address,
        "phone": restaurant.phone,
        "cuisine_categories": restaurant.cuisine_categories,
        "operating_hours": restaurant.operating_hours,
        "contact_person_name": restaurant.contact_person_name,
        "contact_person_role": restaurant.contact_person_role,
        "role": UserRole.RESTAURANT,
        "status": AccountStatus.PENDING,
        "verified": False,
        "documents_submitted": False,
        "documents": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert restaurant
    result = db.restaurants.insert_one(restaurant_doc)
    
    # Generate verification token
    token = generate_verification_token()
    token_doc = {
        "email": restaurant.business_email,
        "token": token,
        "token_type": "email_verification",
        "expires_at": datetime.utcnow() + timedelta(hours=24),
        "created_at": datetime.utcnow()
    }
    db.verification_tokens.insert_one(token_doc)
    
    # Send verification email
    send_verification_email(restaurant.business_email, token, "restaurant")
    
    return {
        "message": "Restaurant account created successfully. Please check your email to verify your account and submit required documents.",
        "restaurant_id": str(result.inserted_id),
        "email": restaurant.business_email
    }

# Email Verification
@router.post("/api/auth/verify", response_model=dict)
async def verify_email(email: str, token: str, account_type: str = "user"):
    """Verify user or restaurant email"""
    
    # Find verification token
    token_doc = db.verification_tokens.find_one({
        "email": email,
        "token": token,
        "token_type": "email_verification"
    })
    
    if not token_doc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Check if token is expired
    if token_doc["expires_at"] < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has expired"
        )
    
    # Update user/restaurant as verified
    collection = db.users if account_type == "user" else db.restaurants
    email_field = "email" if account_type == "user" else "business_email"
    
    result = collection.update_one(
        {email_field: email},
        {
            "$set": {
                "verified": True,
                "status": AccountStatus.ACTIVE if account_type == "user" else AccountStatus.PENDING,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Delete used token
    db.verification_tokens.delete_one({"_id": token_doc["_id"]})
    
    message = "Email verified successfully! Your account is now active." if account_type == "user" else \
              "Email verified successfully! Your account is pending admin review. Please submit required documents."
    
    return {"message": message, "verified": True}

# Resend Verification Email
@router.post("/api/auth/resend-verification", response_model=dict)
async def resend_verification(email: str, account_type: str = "user"):
    """Resend verification email"""
    
    # Find user/restaurant
    collection = db.users if account_type == "user" else db.restaurants
    email_field = "email" if account_type == "user" else "business_email"
    
    account = collection.find_one({email_field: email})
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    if account.get("verified"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is already verified"
        )
    
    # Delete old tokens
    db.verification_tokens.delete_many({
        "email": email,
        "token_type": "email_verification"
    })
    
    # Generate new token
    token = generate_verification_token()
    token_doc = {
        "email": email,
        "token": token,
        "token_type": "email_verification",
        "expires_at": datetime.utcnow() + timedelta(hours=24),
        "created_at": datetime.utcnow()
    }
    db.verification_tokens.insert_one(token_doc)
    
    # Send verification email
    send_verification_email(email, token, account_type)
    
    return {"message": "Verification email sent successfully"}

# Login
@router.post("/api/auth/login", response_model=dict)
async def login(credentials: UserLogin):
    """Login for both users and restaurants"""
    
    # Check in users collection
    user = db.users.find_one({"email": credentials.email})
    if user:
        if not verify_password(credentials.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.get("verified"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please verify your email before logging in"
            )
        
        return {
            "message": "Login successful",
            "user_id": str(user["_id"]),
            "email": user["email"],
            "role": user["role"],
            "full_name": user["full_name"]
        }
    
    # Check in restaurants collection
    restaurant = db.restaurants.find_one({"business_email": credentials.email})
    if restaurant:
        if not verify_password(credentials.password, restaurant["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not restaurant.get("verified"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please verify your email before logging in"
            )
        
        return {
            "message": "Login successful",
            "restaurant_id": str(restaurant["_id"]),
            "email": restaurant["business_email"],
            "role": restaurant["role"],
            "restaurant_name": restaurant["restaurant_name"]
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password"
    )