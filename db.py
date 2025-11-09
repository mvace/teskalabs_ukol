import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv
from models import Base

load_dotenv()

# Budu potřebovat nastavit DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Budu potřebovat nastavit engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Budu potřebovat nastavit session
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
