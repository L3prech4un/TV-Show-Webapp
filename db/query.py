"""query.py: Uses SQLAlchemy to create generic queries for interacting with the Postgres database"""
from db.server import get_session       # import get_session function from server.py

def get_all(table) -> list:
    """Select all records from a table using SQLAlchemy
        args:
            table (object): db table

        returns:
            records (list[obj]): list of records from db table
    """
    session = get_session()
    try:
        # Tries to get all records in the table
        records = session.query(table).all()
        return records
    finally:
        # Closes the session
        session.close()

def insert(record) -> None:
    """ Insert a table record using SQLAlchemy
    
        args:
            record (obj): db table record
    """
    session = get_session()
    try:
        # Tries to add and commit the record to the current session
        session.add(record)
        session.commit()
    except Exception as e:
        # Rollback session if error occurs
        session.rollback()
        print(f"Error inserting record: {e}")
    finally:
        # Closes the session
        session.close()