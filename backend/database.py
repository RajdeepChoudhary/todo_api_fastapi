# backend/database.py

from sqlmodel import SQLModel, create_engine, Session

# ---------------------------
# SQLITE DATABASE CONFIG
# ---------------------------

# sqlite database file name
sqlite_file_name = "database.db"

# sqlite connection url
sqlite_url = f"sqlite:///{sqlite_file_name}"

# engine connects python <-> to database
engine = create_engine(sqlite_url, echo=True)   # echo=True shows queries in terminal


# create all database tables, this will create all tables present in models.py based on SQLModel
def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)


# DB session dependency for FastAPI, Session gives us a connection to the DB
# we wrap it in dependency so fastapi can inject it per request
def get_session():
    with Session(engine) as session:
        yield session
