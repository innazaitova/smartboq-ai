"""
Authentication & Authorization Module
Handles JWT tokens, user authentication, and password hashing
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable must be set in production")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200  # 30 days for production stability

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer token security
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    
    Args:
        data: Dictionary containing user information
        expires_delta: Optional expiration time delta
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and verify JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Dependency to get current authenticated user
    
    Args:
        credentials: Bearer token credentials
    
    Returns:
        User information from token
    
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    
    try:
        payload = decode_access_token(token)
        user_email: str = payload.get("sub")
        user_id: int = payload.get("id")
        
        if user_email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {
            "id": user_id,
            "email": user_email
        }
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Dependency to get current active user (can add additional checks here)
    
    Args:
        current_user: Current user from get_current_user dependency
    
    Returns:
        Active user information
    """
    # Here you can add additional checks like:
    # - User is not banned
    # - Subscription is active
    # - Email is verified
    # etc.
    
    return current_user


def validate_password_strength(password: str) -> bool:
    """
    Validate password meets minimum requirements
    
    Requirements:
    - At least 8 characters
    - Contains uppercase and lowercase
    - Contains at least one number
    
    Args:
        password: Password to validate
    
    Returns:
        True if password is strong enough
    """
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_upper and has_lower and has_digit


def create_reset_token(email: str) -> str:
    """
    Create password reset token
    
    Args:
        email: User email
    
    Returns:
        Reset token (expires in 1 hour)
    """
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {
        "sub": email,
        "type": "reset",
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_reset_token(token: str) -> Optional[str]:
    """
    Verify password reset token
    
    Args:
        token: Reset token
    
    Returns:
        User email if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if payload.get("type") != "reset":
            return None
        
        return payload.get("sub")
    
    except JWTError:
        return None


# Role-based access control
class RoleChecker:
    """Dependency to check user roles"""
    
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles
    
    def __call__(self, user: dict = Depends(get_current_user)):
        # In production, fetch user role from database
        user_role = user.get("role", "user")
        
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        
        return user


# Subscription checker
async def check_subscription_active(user: dict = Depends(get_current_user)):
    """
    Check if user has active subscription
    
    Args:
        user: Current user
    
    Raises:
        HTTPException: If subscription is not active
    """
    # In production, check actual subscription status from database
    # This is a placeholder
    
    subscription_status = user.get("subscription_status", "active")
    
    if subscription_status != "active":
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Subscription required. Please upgrade your plan."
        )
    
    return user


# Rate limiting (basic implementation)
from collections import defaultdict
from time import time

rate_limit_storage = defaultdict(list)

def check_rate_limit(user_id: int, max_requests: int = 100, window_seconds: int = 60) -> bool:
    """
    Simple rate limiting check
    
    Args:
        user_id: User ID
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds
    
    Returns:
        True if under limit, False if over limit
    """
    now = time()
    window_start = now - window_seconds
    
    # Clean old requests
    rate_limit_storage[user_id] = [
        req_time for req_time in rate_limit_storage[user_id]
        if req_time > window_start
    ]
    
    # Check if under limit
    if len(rate_limit_storage[user_id]) >= max_requests:
        return False
    
    # Add current request
    rate_limit_storage[user_id].append(now)
    return True


async def rate_limiter(user: dict = Depends(get_current_user)):
    """Rate limiting dependency"""
    user_id = user["id"]
    
    if not check_rate_limit(user_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    
    return user


# API Key authentication (for integrations)
async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Verify API key for programmatic access
    
    Args:
        credentials: API key credentials
    
    Returns:
        API key information
    """
    api_key = credentials.credentials
    
    # In production, verify against database
    # This is a placeholder
    
    if not api_key.startswith("qb_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return {
        "api_key": api_key,
        "type": "api"
    }
