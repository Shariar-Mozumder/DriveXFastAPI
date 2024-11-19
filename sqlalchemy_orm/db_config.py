from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

DATABASE_URL =  'mssql+pyodbc://DESKTOP-2419RQF/DriveX?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'


engine = create_engine(DATABASE_URL)

# Create metadata
metadata = MetaData()

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

