"""query.py: Uses SQLAlchemy to create generic queries for interacting with the Postgres database"""
from db.server import get_session       # import get_session function from server.py
from sqlalchemy import text
from db.schema.comment import Comment
from db.schema.makes import Makes
from db.schema.post import Post
from db.schema.creates import Creates
from datetime import datetime

def get_User(table, **filters) -> str:
    """Search table for user with matching email and password
        args:
        table (object): db table
        **filters: the attribute(s) to query by

        returns:
            user (object): one user from the db table
    """
    session = get_session()
    try:
        # Get user from User table
        user = session.query(table).filter_by(**filters).first()
        return user
    finally:
        # Close session
        session.close()

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

def getfeed(userid: int) -> list:
    """ Get all posts from users that a user follows, as well as their own posts"""
    session = get_session()
    try:
        query = text(
            """
            SELECT U2."UserID", U2."UName", P1."Title", P1."Date", P1."Content", TV1."Title"
            FROM "user" U1
            JOIN "follows" F ON U1."UserID" = F."UserID"
            JOIN "user" U2 ON F."FollowerID" = U2."UserID"
            JOIN "creates" C1 ON U2."UserID" = C1."UserID"
            JOIN "post" P1 ON C1."PostID" = P1."PostID"
            JOIN "tvmovie" TV1 ON P1."MediaID" = TV1."MediaID"
            WHERE U1."UserID" = :user_id

            UNION

            SELECT U3."UserID", U3."UName", P2."Title", P2."Date", P2."Content", TV2."Title"
            FROM "user" U3
            JOIN "creates" C2 ON U3."UserID" = C2."UserID"
            JOIN "post" P2 ON C2."PostID" = P2."PostID"
            JOIN "tvmovie" TV2 ON P2."MediaID" = TV2."MediaID"
            WHERE U3."UserID" = :user_id

            ORDER BY P1."Date" DESC
            """)
        feed = session.execute(query, {"user_id": userid}).mappings().all()

        return [dict(row) for row in feed]
    
    except Exception as e:
        session.rollback()
        print(f"Error getting feed: {e}")
        return []
    finally:
        session.close()

def getPostComments(postid: int) -> list:
    """ Get all comments on a post """
    session = get_session()
    try:
        query = text(
            """
            SELECT U."Uname", C."Content"
            FROM "user" U
            JOIN "makes" M ON U."UserID" = M."UserID"
            JOIN "post" P ON M."PostID" = P."PostID"
            JOIN "comment" C ON P."PostID" = C."PostID"
            WHERE P."PostID" = :post_id

            ORDER BY C."Date" DESC
            """)
        
        comments = session.execute(query, {"post_id": postid}).mappings().all()
        return [dict(row) for row in comments]
    except Exception as e:
        session.rollback()
        print(f"Error getting post comments: {e}")
        return []
    finally:
        session.close()

def getWatchedTitles(userid: int) -> list:
    """ Return the title of TV/movies the user has watched"""
    session = get_session()
    try:
        query = text(
            """
            SELECT TV."Title"
            FROM "user" U
            JOIN "watched" W ON U."UserID" = W."UserID"
            JOIN "tvmovie" TV ON W."MediaID" = TV."MediaID"
            WHERE W."UserID" = :user_id
            """
        )
        watched = session.execute(query, {"user_id": userid}).mappings.all()
        return [dict(row) for row in watched]
        
    except Exception as e:
        session.rollback()
        print(f"Error getting user watched titles")
        return[]
    finally:
        session.close()

def getWatchingTitles(userid: int) -> list:
    """ Return the title of TV/movies the user is watching"""
    session = get_session()
    try:
        query = text(
            """
            SELECT TV."Title"
            FROM "user" U
            JOIN "watching" W ON U."UserID" = W."UserID"
            JOIN "tvmovie" TV ON W."MediaID" = TV."MediaID"
            WHERE W."UserID" = :user_id
            """
        )
        watching = session.execute(query, {"user_id": userid}).mappings.all()
        return [dict(row) for row in watching]
        
    except Exception as e:
        session.rollback()
        print(f"Error getting user watching titles")
        return[]
    finally:
        session.close()

def getWatchlistTitles(userid: int) -> list:
    """ Return the title of TV/movies the user has on their watchlist"""
    session = get_session()
    try:
        query = text(
            """
            SELECT TV."Title"
            FROM "user" U
            JOIN "watchlist" W ON U."UserID" = W."UserID"
            JOIN "tvmovie" TV ON W."MediaID" = TV."MediaID"
            WHERE W."UserID" = :user_id
            """
        )
        watchlist = session.execute(query, {"user_id": userid}).mappings.all()
        return [dict(row) for row in watchlist]
        
    except Exception as e:
        session.rollback()
        print(f"Error getting user watchlist titles")
        return[]
    finally:
        session.close()
def createPost(userid: int, mediaid: int, title: str, content :str) -> None:
    """Creates a post to add to the database"""
    session = get_session()
    try:
        post = Post(MediaID = mediaid, 
                    Title = title,
                    Date = datetime.now().today().strftime("%Y-%m-%d"),
                    Content = content)
        session.add(post)
        session.flush()

        creates = Creates(UserID = userid, PostID = post.PostID)
        session.add(creates)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error creating a post")
    finally:
        session.close()

def addComment(userid: int, postid: int, content: str) -> None:
    """Add a comment to a post"""
    session = get_session()
    try:
        comment = Comment(
            PostID = postid,
            Date = datetime.now().today().strftime("%Y-%m-%d"),
            Content = content)
        session.add(comment)
        session.flush()

        makes = Makes(UserID = userid, CommentID = comment.CommentID)
        session.add(makes)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding comment to post")
    finally:
        session.close()

def deletePost(userid: int, postid: int) -> None:
    """Allow user to delete a post"""
    session = get_session()
    try:
        query = text(
            """
            DELETE FROM "comment"
            WHERE "PostID" = :post_id
            """)
        session.execute(text(query), {"post_id": postid})

        query = text(
            """
            DELETE FROM "post"
            WHERE "PostID" = :post_id
            """)
        session.execute(text(query), {"post_id": postid})
        session.commit()
    except Exception as e:
        session.rollback()
        print("Error deleting post:", e)
    finally:
        session.close()