from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(
    title="Books CRUD API",
    description="A simple Books CRUD API application deployed on Render",
    version="1.0.0"
)

# Pydantic Schemas
class BookBase(BaseModel):
    title: str = Field(..., json_schema_extra={"example": "The Great Gatsby"})
    author: str = Field(..., json_schema_extra={"example": "F. Scott Fitzgerald"})
    published_year: Optional[int] = Field(None, json_schema_extra={"example": 1925})
    genre: Optional[str] = Field(None, json_schema_extra={"example": "Fiction"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "A classic novel about the American dream."})

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, json_schema_extra={"example": "The Great Gatsby"})
    author: Optional[str] = Field(None, json_schema_extra={"example": "F. Scott Fitzgerald"})
    published_year: Optional[int] = Field(None, json_schema_extra={"example": 1925})
    genre: Optional[str] = Field(None, json_schema_extra={"example": "Fiction"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "Updated description."})

class Book(BookBase):
    id: int

# In-memory database
books_db: dict[int, dict] = {}
current_id: int = 0

@app.get("/")
def read_root():
    return {"message": "Welcome to the Books CRUD API. Visit /docs for the interactive API documentation."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# CRUD Endpoints

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate):
    global current_id
    current_id += 1
    new_book = book_in.model_dump()
    new_book["id"] = current_id
    books_db[current_id] = new_book
    return new_book

@app.get("/books", response_model=List[Book])
def get_books(author: Optional[str] = None, genre: Optional[str] = None):
    results = list(books_db.values())
    if author:
        results = [b for b in results if author.lower() in b["author"].lower()]
    if genre:
        results = [b for b in results if genre.lower() in b["genre"].lower()]
    return results

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return books_db[book_id]

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_in: BookUpdate):
    if book_id not in books_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    
    existing_book = books_db[book_id]
    update_data = book_in.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        existing_book[key] = value
        
    books_db[book_id] = existing_book
    return existing_book

@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    deleted_book = books_db.pop(book_id)
    return deleted_book

