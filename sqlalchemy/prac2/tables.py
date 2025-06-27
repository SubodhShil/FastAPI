from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from urllib.parse import urlparse
import os
import asyncio
import questionary
import sys
from pathlib import Path

# Add the parent directory to sys.path
parent_dir = str(Path(__file__).parent.absolute())
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import models and CRUD modules
import models
from models import meta, students
import create
from create import create_tables_data
import insert
from insert import insert_data_values
import read
from read import read_data_config
import update
from update import update_data_config
import delete
from delete import delete_data_config


load_dotenv()


""" Sqllite for Testing Purposes """

# def get_async_engine():
#     """Setting up the NEON database"""
#     # For testing purposes, use SQLite
#     return create_async_engine(
#         "sqlite+aiosqlite:///students.db",
#         echo=True,
#     )


def get_async_engine():
    """Setting up the NEON database"""
    tmp_postgres = urlparse(os.getenv("DATABASE_URL"))
    engine = create_async_engine(
        f"postgresql+asyncpg://{tmp_postgres.username}:{tmp_postgres.password}@{tmp_postgres.hostname}{tmp_postgres.path}?ssl=require",
        echo=True,
    )
    return engine


async def create_tables(engine):
    """Create tables in the database."""
    data = await create_tables_data()
    print(data["message_start"])
    try:
        async with engine.begin() as conn:
            await conn.run_sync(meta.create_all)
        print(data["message_success"])
    except Exception as e:
        print(data["message_error"].format(error=e))


async def insert_data(engine):
    """Insert sample data into the students table."""
    data = await insert_data_values()
    try:
        async with engine.connect() as conn:
            insert_statement = students.insert().values(**data["sample_data"])
            await conn.execute(insert_statement)
            await conn.commit()
        print(data["message_success"])
    except Exception as e:
        print(data["message_error"].format(error=e))


async def read_data(engine):
    """Select and print all data from the students table."""
    data = await read_data_config()
    try:
        async with engine.connect() as conn:
            select_statement = select(students)
            result = await conn.execute(select_statement)
            rows = result.fetchall()

            if rows:
                print(data["message_header"])
                for row in rows:
                    print(row)
            else:
                print(data["message_empty"])
    except Exception as e:
        print(data["message_error"].format(error=e))


async def update_data(engine):
    """Update a student record."""
    config = await update_data_config()

    try:
        # Get student ID to update
        student_id = await questionary.text(config["prompts"]["id"]).ask_async()
        if not student_id:
            print("Operation cancelled: No ID provided.")
            return

        try:
            student_id = int(student_id)
        except ValueError:
            print("Invalid ID: Please enter a valid number.")
            return

        # Check if student exists
        async with engine.connect() as conn:
            select_stmt = select(students).where(students.c.id == student_id)
            result = await conn.execute(select_stmt)
            student = result.first()

            if not student:
                print(config["message_not_found"].format(id=student_id))
                return

            # Select field to update
            field = await questionary.select(
                config["prompts"]["field"], choices=config["fields"]
            ).ask_async()

            # Get new value
            new_value = await questionary.text(config["prompts"]["value"]).ask_async()
            if not new_value and field != "age":  # Allow empty for non-numeric fields
                print("Operation cancelled: No value provided.")
                return

            # Convert age to int if needed
            if field == "age" and new_value:
                try:
                    new_value = int(new_value)
                except ValueError:
                    print("Invalid age: Please enter a valid number.")
                    return

            # Update student
            stmt = (
                students.update()
                .where(students.c.id == student_id)
                .values(**{field: new_value})
            )

            await conn.execute(stmt)
            await conn.commit()
            print(config["message_success"])

    except Exception as e:
        print(config["message_error"].format(error=e))


async def delete_data(engine):
    """Delete a student record."""
    config = await delete_data_config()

    try:
        # Get student ID to delete
        student_id = await questionary.text(config["prompts"]["id"]).ask_async()
        if not student_id:
            print("Operation cancelled: No ID provided.")
            return

        try:
            student_id = int(student_id)
        except ValueError:
            print("Invalid ID: Please enter a valid number.")
            return

        # Check if student exists
        async with engine.connect() as conn:
            select_stmt = select(students).where(students.c.id == student_id)
            result = await conn.execute(select_stmt)
            student = result.first()

            if not student:
                print(config["message_not_found"].format(id=student_id))
                return

            # Confirm deletion
            confirm = await questionary.confirm(
                config["prompts"]["confirm"]
            ).ask_async()
            if not confirm:
                print("Deletion cancelled.")
                return

            # Delete student
            stmt = students.delete().where(students.c.id == student_id)
            await conn.execute(stmt)
            await conn.commit()
            print(config["message_success"])

    except Exception as e:
        print(config["message_error"].format(error=e))


async def display_menu():
    """Display interactive menu and handle user selection."""
    choices = [
        "Create Tables",
        "Insert Sample Data",
        "Read Data",
        "Update Data",
        "Delete Data",
        "Exit",
    ]

    selection = await questionary.select(
        "Select an operation:", choices=choices
    ).ask_async()

    return selection


async def main():
    """Main function to handle the interactive CLI."""
    engine = get_async_engine()

    try:
        while True:
            selection = await display_menu()

            if selection == "Create Tables":
                await create_tables(engine)
            elif selection == "Insert Sample Data":
                await insert_data(engine)
            elif selection == "Read Data":
                await read_data(engine)
            elif selection == "Update Data":
                await update_data(engine)
            elif selection == "Delete Data":
                await delete_data(engine)
            elif selection == "Exit":
                print("Exiting program...")
                break

            input("\nPress Enter to continue...")
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        await engine.dispose()
        print("Engine disposed.")


if __name__ == "__main__":
    asyncio.run(main())
