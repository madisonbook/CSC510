from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .database import get_database

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials =
                           Depends(security)) -> dict:
    """
    Dependency to get the current authenticated user from token.
    For now, this is a simple implementation. You'll want to add JWT later.
    """
    db = get_database()

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Simple token validation (replace with JWT in production)
    try:
        # Extract token (assuming "Bearer <email>" format temporarily)
        token = credentials.credentials
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
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
