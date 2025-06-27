from fastapi import FastAPI
from routers import discover_and_include_routers

app = FastAPI()


# Automatically discover and include routers from the 'routers.students_router' package
discover_and_include_routers(app, "routers.students_router")
discover_and_include_routers(app, "routers.headers_practice")


@app.get("/")
async def hello():
    return {"message": "Hello Welcome to FastAPI!"}


