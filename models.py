from sqlalchemy import Column, Integer, String
from database import Base

class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    published_year = Column(Integer, nullable=True)
    genre = Column(String, nullable=True, index=True)
    description = Column(String, nullable=True)
