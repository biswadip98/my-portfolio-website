import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Read the database URL from an environment variable.
# Never hardcode credentials — this is the Twelve-Factor principle.
# Example: postgresql+psycopg2://user:password@host:5432/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# The engine manages the actual connection pool to Postgres.
# pool_pre_ping checks a connection is alive before using it,
# which prevents errors from stale connections in production.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# A session factory. Each request gets its own short-lived session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that our ORM models will inherit from.
Base = declarative_base()


# Dependency used by FastAPI routes to get a database session
# and guarantee it is closed after the request finishes.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
