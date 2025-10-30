from sqlalchemy import text
from db.query import get_session  # replace with your module

def reset_all_ids():
    """
    Completely reset all data and IDs in the database tables.
    WARNING: This deletes ALL data in these tables!
    """
    session = get_session()
    try:
        # Truncate tables in the correct order to avoid FK conflicts
        session.execute(text("TRUNCATE TABLE COMMENT CASCADE"))
        session.execute(text("TRUNCATE TABLE CREATES CASCADE"))
        session.execute(text("TRUNCATE TABLE FOLLOWS CASCADE"))
        session.execute(text("TRUNCATE TABLE POST CASCADE"))
        session.execute(text("TRUNCATE TABLE USER CASCADE"))

        # Reset sequences (PostgreSQL)
        session.execute(text("ALTER SEQUENCE user_userid_seq RESTART WITH 1"))
        session.execute(text("ALTER SEQUENCE post_postid_seq RESTART WITH 1"))
        session.execute(text("ALTER SEQUENCE comment_commentid_seq RESTART WITH 1"))
        # Add other sequences if necessary

        session.commit()
        print("All tables truncated and IDs reset.")
    except Exception as e:
        session.rollback()
        print("Error resetting IDs:", e)
    finally:
        session.close()
