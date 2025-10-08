from fastapi import HTTPException, status, Header
from typing import Optional
from .database import get_database

async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """
    Dependency to get the current authenticated user from token.
    For now, this is a simple implementation. You'll want to add JWT later.
    """
    db = get_database()
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Simple token validation (replace with JWT in production)
    try:
        # Extract token (assuming "Bearer <email>" format temporarily)
        token = authorization.replace("Bearer ", "")
        user = await db.users.find_one({"email": token})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        if not user.get("verified"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified"
            )
        
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )