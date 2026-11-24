import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "med_vacancies.db")
raw_db_url = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# Fix PostgreSQL driver resolution:
# Detect available driver (psycopg2 or psycopg 3) to ensure zero ModuleNotFoundError regardless of environment
driver_scheme = "postgresql+psycopg2://"
try:
    import psycopg2
    driver_scheme = "postgresql+psycopg2://"
except ImportError:
    try:
        import psycopg
        driver_scheme = "postgresql+psycopg://"
    except ImportError:
        driver_scheme = "postgresql+psycopg2://"

if raw_db_url.startswith("postgres://"):
    DATABASE_URL = raw_db_url.replace("postgres://", driver_scheme, 1)
elif raw_db_url.startswith("postgresql://") and not raw_db_url.startswith("postgresql+"):
    DATABASE_URL = raw_db_url.replace("postgresql://", driver_scheme, 1)
else:
    DATABASE_URL = raw_db_url

if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

