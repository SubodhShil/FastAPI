import os

from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy.ext.asyncio import create_async_engine
from models import metadata

load_dotenv()


""" Setting up the NEON database """

tmpPostgres = urlparse(os.getenv("DATABASE_URL"))
engine = create_async_engine(
    f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require",
    echo=True,
)


async def get_engine():
    return engine


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
