import os
import asyncio
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    LargeBinary,
    MetaData,
    DateTime,
    text,
)
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy.future import select
from sqlalchemy import insert
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

load_dotenv()
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

engine = create_async_engine(
    f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require",
    echo=True,
)

metadata = MetaData()

documents = Table(
    "documents",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("filename", String, nullable=False),
    Column("filedata", LargeBinary, nullable=False),
    Column("filesize", Integer, nullable=False),
    Column("embedding", Vector(1536), nullable=True),
    Column("uploaded_by", String, nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

async def async_main():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(metadata.drop_all, checkfirst=True)
        await conn.run_sync(metadata.create_all)
    async with engine.connect() as conn:
        pdf_path = "Project Description New Hire.pdf"
        file_size = os.path.getsize(pdf_path)

        if file_size > MAX_FILE_SIZE:
            print(f"Error: File size ({file_size} bytes) exceeds the 50 MB limit.")
            return

        with open(pdf_path, "rb") as f:
            pdf_data = f.read()

        stmt = insert(documents).values(
            filename=pdf_path,
            filedata=pdf_data,
            filesize=file_size,
            uploaded_by="user@example.com",  # Placeholder
        )

        result = await conn.execute(stmt)
        await conn.commit()
        print(f"File {pdf_path} with size {file_size} bytes uploaded successfully.")


if __name__ == "__main__":
    asyncio.run(async_main()) 