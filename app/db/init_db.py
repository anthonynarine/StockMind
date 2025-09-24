# 📁 app/db/init_db.py

from app.db.database import engine, Base
from app.users.models import User  # This ensures the User table is registered

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(init())
