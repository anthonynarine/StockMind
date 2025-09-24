from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 📌 Use async-friendly database URL (SQLite or Postgres)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./stockmind.db")

# ✅ Create an async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Optional: set to False to disable SQL logs
)

# ✅ Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ✅ Declarative base
Base = declarative_base()
