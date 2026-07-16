import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# On Render, DATABASE_URL environment variable is injected automatically.
# Locally, it defaults to a local SQLite database file 'books.db'.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./books.db")

# Workaround for Render's postgres:// vs postgresql:// protocol prefix (SQLAlchemy 1.4+ requires postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configure the SQLite or PostgreSQL connection engine
if DATABASE_URL.startswith("sqlite"):
    # SQLite requires check_same_thread=False for multi-thread support in FastAPI
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to fetch the database session for each request, ensuring cleanup
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
