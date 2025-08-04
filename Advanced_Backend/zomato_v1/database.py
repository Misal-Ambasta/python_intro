# zomato_v1: Database configuration and setup (V1 foundation)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# zomato_v1: Database URL configuration
DATABASE_URL = "sqlite+aiosqlite:///./restaurants.db"

# zomato_v1: Async SQLAlchemy engine and session setup
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# zomato_v1: Base class for SQLAlchemy models
Base = declarative_base()

# zomato_v1: Database dependency for FastAPI
async def get_database():
    async with SessionLocal() as session:
        yield session

# zomato_v1: Function to create database tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)