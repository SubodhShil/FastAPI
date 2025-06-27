from sqlalchemy import MetaData, Column, Table, Integer, String, select
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from urllib.parse import urlparse
import os
import asyncio
import argparse


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


async def create_tables(engine):
    """Create tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)
    print("✅ Tables created successfully.")


async def insert_data(engine):
    """Insert sample data into the students table."""
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


async def select_data(engine):
    """Select and print all data from the students table."""
    async with engine.connect() as conn:
        select_statement = select(students)
        result = await conn.execute(select_statement)
        print("📝 Students data:")
        for row in result.fetchall():
            print(row)


async def main():
    """Main function to parse arguments and run database operations."""
    parser = argparse.ArgumentParser(description="Manage database operations.")
    parser.add_argument("action", choices=["create", "insert", "select"], help="The action to perform.")
    args = parser.parse_args()

    engine = get_async_engine()
    try:
        if args.action == "create":
            await create_tables(engine)
        elif args.action == "insert":
            await insert_data(engine)
        elif args.action == "select":
            await select_data(engine)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        await engine.dispose()
        print("Engine disposed.")


if __name__ == "__main__":
    asyncio.run(main())
