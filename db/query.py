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

def getFeed(userid: int) -> list:
    """ Get all posts from users that a user follows, as well as their own posts"""
    session = get_session()
    try:
        query = text(
            """
            SELECT U2."UserID" AS userid, U2."UName" AS username, P1."PostID" AS postid, P1."Title" AS post_title, 
                P1."Date" AS post_date, P1."Content" AS post_content, TV1."Title" AS media_title
            FROM "user" U1
            JOIN "follows" F ON U1."UserID" = F."UserID"
            JOIN "user" U2 ON F."FollowerID" = U2."UserID"
            JOIN "creates" C1 ON U2."UserID" = C1."UserID"
            JOIN "post" P1 ON C1."PostID" = P1."PostID"
            JOIN "tvmovie" TV1 ON P1."MediaID" = TV1."MediaID"
            WHERE U1."UserID" = :user_id

            UNION

            SELECT U3."UserID" AS userid, U3."UName" AS username, P2."PostID" AS postid, P2."Title" AS post_title,
                P2."Date" AS post_date, P2."Content" AS post_content, TV2."Title"
            FROM "user" U3
            JOIN "creates" C2 ON U3."UserID" = C2."UserID"
            JOIN "post" P2 ON C2."PostID" = P2."PostID"
            JOIN "tvmovie" TV2 ON P2."MediaID" = TV2."MediaID"
            WHERE U3."UserID" = :user_id

            ORDER BY post_date DESC
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
            SELECT U."UName" AS username, C."Content" AS comment_content
            FROM "comment" C
            JOIN "post" P ON C."PostID" = P."PostID"
            JOIN "makes" M ON C."CommentID" = M."CommentID"
            JOIN "user" U ON M."UserID" = U."UserID"
            WHERE P."PostID" = :post_id

            ORDER BY C."Date" DESC
            """)
        
        comments = session.execute(query, {"post_id": postid}).mappings().all()
        return [dict(row) for row in comments]
    except Exception as e:
        session.rollback()
        print(f"Error getting post comments:", e)
        return []
    finally:
        session.close()

def getWatchedTitles(userid: int) -> list:
    """ Return the title of TV/movies the user has watched"""
    session = get_session()
    try:
        query = text(
            """
            SELECT TV."Title" AS watched_title
            FROM "user" U
            JOIN "watched" W ON U."UserID" = W."UserID"
            JOIN "tvmovie" TV ON W."MediaID" = TV."MediaID"
            WHERE W."UserID" = :user_id
            """
        )
        watched = session.execute(query, {"user_id": userid}).mappings().all()
        return [row["watched_title"] for row in watched]
        
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
            SELECT TV."Title" AS watching_title
            FROM "user" U
            JOIN "watching" W ON U."UserID" = W."UserID"
            JOIN "tvmovie" TV ON W."MediaID" = TV."MediaID"
            WHERE W."UserID" = :user_id
            """
        )
        watching = session.execute(query, {"user_id": userid}).mappings().all()
        return [row["watching_title"] for row in watching]
        
    except Exception as e:
        session.rollback()
        print(f"Error getting user watching titles", e)
        return[]
    finally:
        session.close()

def getWatchlistTitles(userid: int) -> list:
    """ Return the title of TV/movies the user has on their watchlist"""
    session = get_session()
    try:
        query = text(
            """
            SELECT TV."Title" AS watchlist_title
            FROM "user" U
            JOIN "watchlist" W ON U."UserID" = W."UserID"
            JOIN "tvmovie" TV ON W."MediaID" = TV."MediaID"
            WHERE W."UserID" = :user_id
            """
        )
        watchlist = session.execute(query, {"user_id": userid}).mappings().all()
        return [row["watchlist_title"] for row in watchlist]
        
    except Exception as e:
        session.rollback()
        print(f"Error getting user watchlist titles", e)
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

        session.execute(Creates.insert().values(UserID = userid, PostID = post.PostID))
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error creating a post", e)
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

        session.execute(Makes.insert().values(UserID = userid, CommentID = comment.CommentID))
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding comment to post", e)
    finally:
        session.close()

def deletePost(postid: int) -> None:
    """Allow user to delete a post"""
    session = get_session()
    try:
        query = text(
            """
            DELETE FROM "makes"
            WHERE "CommentID" IN (
                SELECT "CommentID" FROM "comment" WHERE "PostID" =:post_id
            )
            """)
        session.execute(query, {"post_id": postid})

        query = text(
            """
            DELETE FROM "comment"
            WHERE "PostID" = :post_id
            """)
        session.execute(query, {"post_id": postid})

        query = text(
            """
            DELETE FROM "creates"
            WHERE "PostID" = :post_id
            """
        )
        session.execute(query, {"post_id": postid})
        
        query = text(
            """
            DELETE FROM "post"
            WHERE "PostID" = :post_id
            """)
        session.execute(query, {"post_id": postid})
        session.commit()
    except Exception as e:
        session.rollback()
        print("Error deleting post:", e)
    finally:
        session.close()
    
def get_all_users_except_current(user_id: int) -> list:
    """Get all users except the current user for follow suggestions"""
    session = get_session()
    try:
        query = text("""
        SELECT "UserID", "UName", "FName", "LName"
        FROM "user"
        WHERE "UserID" != :user_id
        AND "UserID" NOT IN (
            SELECT "FollowerID" FROM "follows" WHERE "UserID" = :user_id
        )
        ORDER BY "UName"
        """)
        result = session.execute(query, {"user_id": user_id})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        print("Error getting users:", e)
        return []
    finally:
        session.close()

def follow_user(user_id: int, follower_id: int) -> bool:
    """Follow another user"""
    session = get_session()
    try:
        # Check if already following
        check_query = text("""
        SELECT 1 FROM "follows" 
        WHERE "UserID" = :user_id AND "FollowerID" = :follower_id
        """)
        existing = session.execute(check_query, {
            "user_id": user_id, 
            "follower_id": follower_id
        }).first()
        
        if existing:
            return False  # Already following
        
        # Insert follow relationship
        insert_query = text("""
        INSERT INTO "follows" ("UserID", "FollowerID")
        VALUES (:user_id, :follower_id)
        """)
        session.execute(insert_query, {
            "user_id": user_id,
            "follower_id": follower_id
        })
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error following user:", e)
        return False
    finally:
        session.close()

def unfollow_user(user_id: int, follower_id: int) -> bool:
    """Unfollow a user"""
    session = get_session()
    try:
        query = text("""
        DELETE FROM "follows" 
        WHERE "UserID" = :user_id AND "FollowerID" = :follower_id
        """)
        result = session.execute(query, {
            "user_id": user_id,
            "follower_id": follower_id
        })
        session.commit()
        return result.rowcount > 0
    except Exception as e:
        session.rollback()
        print("Error unfollowing user:", e)
        return False
    finally:
        session.close()

def get_following(user_id: int) -> list:
    """Get users that the current user is following"""
    session = get_session()
    try:
        query = text("""
        SELECT U."UserID", U."UName", U."FName", U."LName"
        FROM "follows" F
        JOIN "user" U ON F."FollowerID" = U."UserID"
        WHERE F."UserID" = :user_id
        ORDER BY U."UName"
        """)
        result = session.execute(query, {"user_id": user_id})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        print("Error getting following list:", e)
        return []
    finally:
        session.close()

def get_followers(user_id: int) -> list:
    """Get users who are following the current user"""
    session = get_session()
    try:
        query = text("""
        SELECT U."UserID", U."UName", U."FName", U."LName"
        FROM "follows" F
        JOIN "user" U ON F."UserID" = U."UserID"
        WHERE F."FollowerID" = :user_id
        ORDER BY U."UName"
        """)
        result = session.execute(query, {"user_id": user_id})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        print("Error getting followers list:", e)
        return []
    finally:
        session.close()

def is_following(user_id: int, target_user_id: int) -> bool:
    """Check if user is following another user"""
    session = get_session()
    try:
        query = text("""
        SELECT 1 FROM "follows" 
        WHERE "UserID" = :user_id AND "FollowerID" = :target_user_id
        """)
        result = session.execute(query, {
            "user_id": user_id,
            "target_user_id": target_user_id
        }).first()
        return result is not None
    except Exception as e:
        print("Error checking follow status:", e)
        return False
    finally:
        session.close()

def addToWatched(userid: int, mediaid: int) -> None:
    """Add a show to the user's watched list using SQLAlchemy only."""
    session = get_session()
    try:
        session.execute(
            text("""
                INSERT INTO "watched" ("UserID", "MediaID")
                VALUES (:user_id, :media_id)
                ON CONFLICT DO NOTHING;
            """),
            {"user_id": userid, "media_id": mediaid}
        )
        session.commit()
    except Exception as e:
        session.rollback()
        print("Error adding to watched list:", e)
    finally:
        session.close()

def removeFromWatched(userid:int, title:str) -> None:
    """Remove a show from the user's watched list."""
    session = get_session()
    try:
        mediaid = session.execute(text('SELECT "MediaID" FROM "tvmovie" WHERE "Title" = :title'),{"title": title}).scalar()
        
        if mediaid:
            session.execute(text('DELETE FROM "watched" WHERE "UserID" = :user_id AND "MediaID" = :media_id'),{"user_id": userid, "media_id": mediaid})
            session.commit()

    except Exception as e:
        session.rollback()
        print("Error removing from watched:", e)
    finally:
        session.close()

def addToCurrentlyWatching(userid: int, mediaid:int) -> None:
    """Add a show to the user's currently watching list using SQLAlchemy only."""
    session = get_session()
    try:
        session.execute(
            text("""
                INSERT INTO "watching" ("UserID", "MediaID")
                VALUES (:user_id, :media_id)
                ON CONFLICT DO NOTHING;
            """),
            {"user_id": userid, "media_id": mediaid}
        )
        session.commit()
    except Exception as e:
        session.rollback()
        print("Error adding to currently watching list:", e)
    finally:
        session.close()

def removeFromCurrentlyWatching(userid: int, title: str) -> None:
    """Remove a show from the user's currently watching list."""
    session = get_session()
    try:
        mediaid = session.execute(text('SELECT "MediaID" FROM "tvmovie" WHERE "Title" = :title'),{"title": title}).scalar()
        if mediaid:
            session.execute(text('DELETE FROM "watching" WHERE "UserID" = :user_id AND "MediaID" = :media_id'),{"user_id": userid, "media_id": mediaid})
            session.commit()
    except Exception as e:
        session.rollback()
        print("Error removing from currently watching:", e)
        return False
    finally:
        session.close()

def addToWatchlist(userid, mediaid):
    """Add a show to the user's watchlist using SQLAlchemy only."""
    session = get_session()
    try:
        session.execute(
            text("""
                INSERT INTO "watchlist" ("UserID", "MediaID")
                VALUES (:user_id, :media_id)
                ON CONFLICT DO NOTHING;
            """),
            {"user_id": userid, "media_id": mediaid}
        )

        session.commit()
    except Exception as e:
        session.rollback()
        print("Error adding to watchlist:", e)
    finally:
        session.close()

def removeFromWatchlist(userid, title) -> None:
    """Remove a show from the user's watchlist."""
    session = get_session()
    try:
        mediaid = session.execute(text('SELECT "MediaID" FROM "tvmovie" WHERE "Title" = :title'),{"title": title}).scalar()
        if mediaid:
            session.execute(text('DELETE FROM "watchlist" WHERE "UserID" = :user_id AND "MediaID" = :media_id'),{"user_id": userid, "media_id": mediaid})
            session.commit()
    except Exception as e:
        session.rollback()
        print("Error removing from watchlist:", e)
    finally:
        session.close()