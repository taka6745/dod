import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Define the path to the .env file (two folders above the current file)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Get each part of the database URL from the .env file
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construct the full DATABASE_URL string
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Configure the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency for getting a database session.
    Yields a database session and ensures it's closed after usage.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
