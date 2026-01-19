from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
from config import Config

#BASE_DIR = Path(__file__).resolve().parent.parent.parent
#DB_PATH = BASE_DIR / "user.db"
#SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
SQLALCHEMY_DATABASE_URL = Config.DATABASE_URL

connect_args = {"check_same_thread": False} # This is for sqlite only

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

sessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_table():
    Base.metadata.create_all(bind=engine)