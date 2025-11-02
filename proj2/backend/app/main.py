from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import asyncio
from datetime import datetime
from .database import connect_to_mongo, close_mongo_connection, get_database
from .auth_routes import router as auth_router
from .user_routes import router as user_router
from .meal_routes import router as meal_router
from pymongo import ASCENDING
from pymongo import ASCENDING
from . import seed_data

async def wait_for_mongo(retries: int = 60, delay: float = 1.0):
    db = get_database()
    for _ in range(retries):
        try:
            await db.command("ping")
            return
        except Exception:
            await asyncio.sleep(delay)
    raise RuntimeError("MongoDB not ready after waiting")

async def run_seed_once():
    db = get_database()
    if await db["_meta"].find_one({"key": "seed_done"}):
        return
    await seed_data.seed()
    await db["_meta"].insert_one({"key": "seed_done", "at": datetime.utcnow()})


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    await wait_for_mongo()
    await run_seed_once()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="Taste Buddies API",
    description="A full-stack application with FastAPI, MongoDB, and React",
    version="1.0.0",
    lifespan=lifespan
)

@app.on_event("startup")
async def startup_event():
    """Initialize database indexes on application startup"""
    
    await connect_to_mongo()
    db = get_database()
    
    if db is not None:
        try:
            # User indexes
            await db.users.create_index([("email", ASCENDING)], unique=True)
            
            # Meal indexes
            await db.meals.create_index([("seller_id", ASCENDING)])
            await db.meals.create_index([("status", ASCENDING)])
            await db.meals.create_index([("cuisine_type", ASCENDING)])
            await db.meals.create_index([("created_at", ASCENDING)])
            
            # Verification token indexes
            await db.verification_tokens.create_index([("expires_at", ASCENDING)], expireAfterSeconds=0)
            await db.verification_tokens.create_index([("email", ASCENDING)])
            
            # Review indexes
            await db.reviews.create_index([("meal_id", ASCENDING)])
            await db.reviews.create_index([("reviewer_id", ASCENDING)])
            await db.reviews.create_index([("seller_id", ASCENDING)])
            
            print("✅ Database indexes verified/created")
        except Exception as e:
            print(f"⚠️ Index creation note: {e}")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    await close_mongo_connection()

# Include routersv
app.include_router(auth_router, tags =["Authentication"])
app.include_router(user_router)
app.include_router(meal_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Taste Buddiez API",
        "tagline": "Connecting neighbors through homemade meals"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}