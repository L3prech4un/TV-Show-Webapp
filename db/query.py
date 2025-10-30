"""query.py: Uses SQLAlchemy to create generic queries for interacting with the Postgres database"""
from db.server import get_session       # import get_session function from server.py
from sqlalchemy import text 

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

def changePost(userid: int, postid: int, newContent: str) -> bool:
    "Allow User to change the text of what they post"
    session = get_session()
    try:
        # Tries to update the post 
        query = """
        UPDATE POST
        SET CONTENT = :NEWCONTENT
        WHERE POSTID = :POSTID
        AND POSTID IN (
            SELECT C.POSTID
            FROM CREATES C
            WHERE C.USERID = :USERID);
        """
        session.execute(text(query), {"USERID": userid, "POSTID": postid, "NEWCONTENT": newContent })
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error Updating post:", e)
        return False
    finally:
        session.close()
    
def deletePost(userid: int, postid: int) -> bool:
    "Allow User to delete a post"
    session = get_session()
    try:
        # Tries to delete the post
        session.execute("""DELETE COMMENT WHERE POSTID = :POSTID""", {"POSTID": postid})
       
        session.execute(
        """
            DELETE POST WHERE POSTID = :POSTID
            AND POSTID IN (
            SELECT C.POSTID
            FROM CREATES C
            WHERE C.USERID = :USERID);
        """,
        {"POSTID": postid, "USERID": userid})

        session.execute("""DELETE CREATES WHERE POSTID = :POSTID;""", {"POSTID": postid})

        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error Deleting Post:", e)
        return False

def getFeed(userid: int) -> list:
    "Create the Users feed from the people they follow"
    session = get_session()
    try:
        # Tries to make a User's feed from follower posts
        query = """
        SELECT P.TITLE, P.DATE, P.CONTENT 
        FROM USER U1, USER U2, FOLLOWS F, CREATES C, POST P
        WHERE U1.USERID = F.USERID
        AND F.FOLLOWERID = U2.USERID
        AND U2.USERID = C.USERID
        AND C.POSTID = P.POSTID
        AND U1.USERID = :USER_ID

        UNION

        SELECT P.TITLE, P.DATE, P.CONTENT
        FROM CREATES C, POST P
        WHERE C.USERID = :USER_ID
        AND C.POSTID = P.POSTID
        
        ORDER BY DATE DESC;
        """
        result = session.execute(text(query), {"USER_ID": userid}).fetchall()
        return result
    except Exception as e:
        session.rollback()
        print("Error loading feed:", e)
    finally:
        session.close()