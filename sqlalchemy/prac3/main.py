import asyncio
from create_table import get_engine, create_tables
from sqlalchemy import text


async def main():
    engine = await get_engine()
    async with engine.connect() as conn:
        result = await conn.execute(text("select 'hello world'"))
        print(result.fetchall())
    await engine.dispose()

    # creating tables
    await create_tables(engine)
    print("✅ Tables created successfully.")


if __name__ == "__main__":
    asyncio.run(main())
