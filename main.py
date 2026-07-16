from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import BookDB

# Create tables in the database if they don't already exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Books CRUD API",
    description="A simple Books CRUD API application deployed on Render",
    version="1.0.0"
)

# Pydantic Schemas for Request/Response validation
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

    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return {"message": "Welcome to the Books CRUD API. Visit /docs for the interactive API documentation."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# CRUD Endpoints

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, db: Session = Depends(get_db)):
    db_book = BookDB(**book_in.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books", response_model=List[Book])
def get_books(author: Optional[str] = None, genre: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(BookDB)
    if author:
        query = query.filter(BookDB.author.ilike(f"%{author}%"))
    if genre:
        query = query.filter(BookDB.genre.ilike(f"%{genre}%"))
    return query.all()

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return db_book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_in: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    
    update_data = book_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
        
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    db.delete(db_book)
    db.commit()
    return db_book


