import asyncio
from sqlalchemy import insert
from models import employee
from create_table import engine


async def insert_values() -> None:
    insert_statement = insert(employee).values(
        name="Subodh Chandr Shil",
        age=33,
        email="subodh@gmail.com",
        phone="01533491807",
        address="Dhaka, Bangladesh",
        department="IT",
        position="Software Engineer",
        salary=33000,
    )

    async with engine.connect() as conn:
        await conn.execute(insert_statement)
        await conn.commit()

    print("✅ Data inserted successfully!!")

asyncio.run(insert_values())