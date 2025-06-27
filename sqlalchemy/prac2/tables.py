from sqlalchemy import MetaData, Column, Table, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from urllib.parse import urlparse
import os
import asyncio


load_dotenv()


def get_async_engine():
    """Setting up the NEON database"""
    tmp_postgres = urlparse(os.getenv("DATABASE_URL"))
    engine = create_async_engine(
        f"postgresql+asyncpg://{tmp_postgres.username}:{tmp_postgres.password}@{tmp_postgres.hostname}{tmp_postgres.path}?ssl=require",
        echo=True,
    )
    return engine


meta = MetaData()


students = Table(
    "students",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("age", Integer),
    Column("gender", String),
    Column("email", String),
    Column("phone", String),
    Column("address", String),
    Column("city", String),
    Column("state", String),
)


async def main():
    """Create tables and insert data."""
    engine = get_async_engine()
    try:
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(meta.create_all)
        print("✅ Tables created successfully.")

        # Insert data
        async with engine.connect() as conn:
            insert_statement = students.insert().values(
                name="John Doe",
                age=20,
                gender="Male",
                email="john.doe@example.com",
                phone="1234567890",
                address="123 Main St",
                city="Anytown",
                state="CA",
            )
            await conn.execute(insert_statement)
            await conn.commit()
        print("✅ Data inserted successfully.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        await engine.dispose()
        print("Engine disposed.")


if __name__ == "__main__":
    asyncio.run(main())
