from sqlalchemy import MetaData, Table, Column, Integer, String


metadata = MetaData()

""" employee model """
employee = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("age", Integer, nullable=False),
    Column("email", String, nullable=False),
    Column("phone", String, nullable=False),
    Column("address", String, nullable=False),
    Column("department", String, nullable=False),
    Column("position", String, nullable=False),
    Column("salary", Integer, nullable=False),
)