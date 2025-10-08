from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import connect_to_mongo, close_mongo_connection, get_database
from .auth_routes import router as auth_router
from pymongo import ASCENDING



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="FastAPI MongoDB Application",
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
            # Create indexes (will skip if already exist)
            await db.users.create_index([("email", ASCENDING)], unique=True)
            await db.restaurants.create_index([("business_email", ASCENDING)], unique=True)
            await db.verification_tokens.create_index([("expires_at", ASCENDING)], expireAfterSeconds=0)
            await db.verification_tokens.create_index([("email", ASCENDING)])
            print("✅ Database indexes verified/created")
        except Exception as e:
            print(f"⚠️ Index creation note: {e}")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    await close_mongo_connection()

# Include routersv
app.include_router(auth_router, tags =["Authentication"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MongoDB!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}