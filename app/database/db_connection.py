from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.app_config import DATABASE_URL

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    # Required for multithreaded SQLite
    connect_args={"check_same_thread": False},
    # Set to True if you want SQL logs
    echo=False,
)

# Session factory (synchronous)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for ORM models
Base = declarative_base()


# Initialize the database
#   – Creates the file and the “requests” table on first run
def init_db() -> None:
    """
    Call this once at application startup to create the SQLite file
    and all tables declared in SQLAlchemy models.
    """
    # Import models here so they are registered before create_all()
    from app.models import calculation_model  # noqa: F401

    Base.metadata.create_all(bind=engine)


# FastAPI dependency that yields a DB session
def get_db():
    """
    FastAPI dependency:
    Opens a database session and closes it after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
