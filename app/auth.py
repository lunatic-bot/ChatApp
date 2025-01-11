from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from models import User
from schemas import UserCreate, UserResponse
from passlib.hash import bcrypt

auth_router = APIRouter()

def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = bcrypt.hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    print('New user : ', new_user)
    return new_user
