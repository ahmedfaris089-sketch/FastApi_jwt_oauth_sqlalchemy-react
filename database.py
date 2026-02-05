from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite (Development)
DATABASE_URL = "sqlite:///./auth.db"

# PostgreSQL (Production)
# DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


