import os, asyncio
from sqlalchemy import Column, Integer, String, MetaData, Table
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

engine = create_async_engine(
    f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require",
    echo=True,
)

metadata = MetaData()

people = Table(
    "people",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("age", Integer, nullable=False),
)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


asyncio.run(async_main())
