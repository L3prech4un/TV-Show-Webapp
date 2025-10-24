"""server.py: connect to Postgres database and create tables"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# load environment variables from .env
load_dotenv()

# declarative base is sqlalchemy's foundation class that enables you to create 
# database models using python classes instead of manually defining tables
Base = declarative_base()

# database connection - values set in .env
db_name = os.getenv('db_name')
db_owner = os.getenv('db_owner')
db_pass = os.getenv('db_pass')
db_url = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"

engine = create_engine(db_url)

# a session is a workspace for your database operations
PostgresSession = sessionmaker(
    autocommit=False, # you control when changes are saved
    autoflush=False, # you control when sql queries are sent
    bind=engine # how the session knows which db to connect to
)

def get_session():
    """Get a database session"""
    return PostgresSession()

def init_database():
    """Initialize database tables"""
    try:
        # import all of the tables
        from db.schema import Users
        
        # create all of the tables
        Base.metadata.create_all(bind=engine)
        print(f"\n\n----------- Connection successful!")
        print(f" * Connected to database: {db_name}")
        print(f" * Database tables created successfully!")
        return True

    # print the error if the connection attempt fails
    except Exception as error:
        print(f"\n\n----------- Connection failed!")
        print(f" * Unable to connect to database: {db_name}")
        print(f" * ERROR: {error}")
        return False