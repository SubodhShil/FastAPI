from sqlalchemy import MetaData, Column, Table, Integer, String

# Define metadata
meta = MetaData()

# Define students table
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