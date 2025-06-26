from fastapi import FastAPI, Header, status, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import json


app = FastAPI()


with open("book.json", "r") as f:
    books = json.load(f)


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


""" GET REQUESTS """


@app.get("/")
async def home():
    return {"message": "Welcome to the API"}


@app.get("/books", response_model=List[Book])
async def get_all_books() -> dict:
    return books


# get a book by id
@app.get("/books/{id}")
async def get_single_book(id: int) -> dict:
    return next(
        (book for book in books if book["id"] == id),
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"),
    )


""" POST REQUESTS """


@app.post("/books/add_book", response_model=Book, status_code=status.HTTP_201_CREATED)
async def add_book(book: BookCreateModel) -> dict:
    new_id = max((b["id"] for b in books), default=0) + 1

    new_book = {
        "id": new_id,
        "title": book.title,
        "author": book.author,
        "publisher": book.publisher,
        "published_date": book.published_date,
        "page_count": book.page_count,
        "language": book.language,
    }

    books.append(new_book)

    with open("book.json", "w") as f:
        json.dump(books, f, indent=4)

    return new_book


@app.patch("/books/{id}", response_model=Book)
async def update_book(
    id: int, book_update: BookUpdateModel, status_code=status.HTTP_200_OK
) -> dict:
    book_to_update = next((book for book in books if book["id"] == id), None)

    if book_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            book_to_update[key] = value

    with open("book.json", "w") as f:
        json.dump(books, f, indent=4)

    return book_to_update


@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
