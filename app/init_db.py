# This creates all tables that are defined in your models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from database import async_engine
from models import Base



# Assuming async_engine is your asynchronous engine
async def recreate_tables():
    async with async_engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


import asyncio

asyncio.run(recreate_tables())