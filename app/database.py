from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import os
from dotenv import load_dotenv
from pathlib import Path
from databases import Database

env_path = Path(__file__).parent.parent / '.env'
print('Env path : ', env_path)

load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")  
print('Database URL : ', DATABASE_URL)


# For async database connection
database = Database(DATABASE_URL)
metadata = MetaData()

# SQLAlchemy models
Base = declarative_base()

# Create an async SQLAlchemy engine
async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency to get the async database session
async def get_db() -> AsyncSession: # type: ignore 
    async with AsyncSessionLocal() as session:
        yield session

