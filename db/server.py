"""server.py: connect to Postgre database and create tables"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env
load_dotenv()

Base = declarative_base()

# database values
db_name = os.getenv('db_name')
db_owner = os.getenv('db_owner')
db_pass = os.getenv('db_pass')
db_url = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"

engine = create_engine(db_url)

PostgresSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_session():
    """Get database session"""
    return PostgresSession()

def init_database():
    """Initialize database tables"""
    try:
        # Import all of the tables
        from db.schema.comment import Comment
        from db.schema.post import Post
        from db.schema.tvmovie import TVMovie
        from db.schema.user import User
        from db.schema.follows import Follows
        from db.schema.creates import Creates
        from db.schema.makes import Makes
        from db.schema.watched import Watched
        from db.schema.watching import Watching
        from db.schema.watchlist import Watchlist

        # Create all of the tables
        Base.metadata.create_all(bind=engine)
        print(f"\n\n----------- Connection successful!")
        print(f" * Connected to {db_name}")
        print(f" * Successfully created DB tables!")
        return True
    except Exception as error:
        print(f"\n\n----------- Connection failed!")
        print(f" * Unable to connect to {db_name}")
        print(f" * ERROR: {error}")
        return False