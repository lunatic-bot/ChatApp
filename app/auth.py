from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from models import User
from schemas import UserCreate, UserResponse
from passlib.hash import bcrypt

# Create an APIRouter instance for authentication-related endpoints
auth_router = APIRouter()

# Dependency to get an async database session
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db  # Yield the session for dependency injection
        await db.close()  # Ensure the session is closed after use

@auth_router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Registers a new user by:
    1. Hashing the provided password.
    2. Creating a new User instance.
    3. Adding and committing the user to the database.
    4. Returning the created user.

    Args:
        user (UserCreate): The user details received in the request body.
        db (AsyncSession): The database session dependency.

    Returns:
        UserResponse: The created user details (excluding the password).
    """

    # Hash the user's password using bcrypt
    hashed_password = bcrypt.hash(user.password)

    # Create a new user instance with the hashed password
    new_user = User(username=user.username, hashed_password=hashed_password)

    # Add the new user to the database session
    db.add(new_user)
    
    # Commit the transaction to save the user in the database
    await db.commit()

    # Refresh the user instance to get updated values from the database
    await db.refresh(new_user)
    return new_user  # Return the created user (response schema ensures sensitive data is excluded)
