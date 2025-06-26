from sqlalchemy import create_engine, text

# Create a database and connect to it
engine = create_engine("sqlite:///firstdb.db", echo=True)
conn = engine.connect()


conn.execute(
    text(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)"
    )
)

conn.commit()

from sqlalchemy.orm import Session

session = Session(engine)

session.execute(
    text("INSERT INTO users (name, email) VALUES (:name, :email)"),
    {"name": "Subodh Chandra Shil", "email": "subodh@gmail.com"},
)
session.commit()