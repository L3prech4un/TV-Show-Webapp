"""query.py: Uses SQLAlchemy to create generic queries for interacting with the Postgres database"""
from db.server import get_session       # import get_session function from server.py
from sqlalchemy import text 

def get_User(table, **filters) -> str:
    """Search table for user with matching email and password (keeps ORM query)"""
    session = get_session()
    try:
        # Get user from User table
        user = session.query(table).filter_by(**filters).first()
        return user
    finally:
        # Close session
        session.close()

def get_all(table, **filters) -> list:
    """Select all records from a table using SQLAlchemy
        args:
            table (object): db table
            **filters: optional filters, e.g. UserID=1, MediaID=2

        returns:
            records (list[obj]): list of records from db table
    """
    session = get_session()
    try:
        query = session.query(table)
        if filters:
            query = query.filter_by(**filters)
        return query.all()
    finally:
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
        query = text("""
        UPDATE "post"
        SET "Content" = :new_content
        WHERE "PostID" = :post_id
          AND "PostID" IN (
            SELECT "PostID" FROM "creates" WHERE "UserID" = :user_id
          );
        """)
        params = {"user_id": userid, "post_id": postid, "new_content": newContent}
        session.execute(query, params)
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
        # delete comments
        session.execute(text('DELETE FROM "comment" WHERE "PostID" = :post_id;'), {"post_id": postid})

        # delete creates associations (if any)
        session.execute(text('DELETE FROM "creates" WHERE "PostID" = :post_id;'), {"post_id": postid})

        # delete the post only if the user owns it
        session.execute(text("""
            DELETE FROM "post"
            WHERE "PostID" = :post_id
              AND "PostID" IN (
                SELECT "PostID" FROM "creates" WHERE "UserID" = :user_id
              );
        """), {"post_id": postid, "user_id": userid})

        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error Deleting Post:", e)
        return False
    finally:
        session.close()

def getFeed(userid: int) -> list:
    """Return list of dicts with post data including MediaID, media title, and creator's UserID"""
    session = get_session()
    try:
        query = text("""
        SELECT P."PostID" AS postid,
               P."Title" AS title, 
               P."Date" AS date, 
               P."Content" AS content,
               U2."UName" AS username,
               U2."UserID" AS userid,
               T."Title" AS media_title
        FROM "user" U1
        JOIN "follows" F ON U1."UserID" = F."UserID"
        JOIN "user" U2 ON F."FollowerID" = U2."UserID"
        JOIN "creates" C ON U2."UserID" = C."UserID"
        JOIN "post" P ON C."PostID" = P."PostID"
        JOIN "tvmovie" T ON P."MediaID" = T."MediaID"
        WHERE U1."UserID" = :user_id

        UNION

        SELECT P."PostID" AS postid,
               P."Title" AS title, 
               P."Date" AS date, 
               P."Content" AS content,
               U."UName" AS username,
               U."UserID" AS userid,
               T."Title" AS media_title
        FROM "creates" C
        JOIN "post" P ON C."PostID" = P."PostID"
        JOIN "user" U ON C."UserID" = U."UserID"
        JOIN "tvmovie" T ON P."MediaID" = T."MediaID"
        WHERE C."UserID" = :user_id

        ORDER BY date DESC;
        """)
        rows = session.execute(query, {"user_id": userid}).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        print("Error loading feed:", e)
        return []
    finally:
        session.close()


def addComment(userid: int, postid: int, content: str) -> bool:
    """Add a comment to a post using pure SQL"""
    session = get_session()
    try:
        # Insert comment
        comment_query = text("""
        INSERT INTO "comment" ("PostID", "Content")
        VALUES (:post_id, :content)
        RETURNING "CommentID"
        """)
        
        result = session.execute(comment_query, {
            "post_id": postid,
            "content": content
        })
        comment_id = result.scalar()

        # Create Makes association
        makes_query = text("""
        INSERT INTO "makes" ("UserID", "CommentID")
        VALUES (:user_id, :comment_id)
        """)
        
        session.execute(makes_query, {
            "user_id": userid,
            "comment_id": comment_id
        })
        
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error adding comment:", e)
        return False
    finally:
        session.close()

def getPostComments(postid: int) -> list:
    """Get all comments for a post using pure SQL"""
    session = get_session()
    try:
        query = text("""
        SELECT C."Content" as content,
               U."UName" as username
        FROM "comment" C
        JOIN "makes" M ON C."CommentID" = M."CommentID"
        JOIN "user" U ON M."UserID" = U."UserID"
        WHERE C."PostID" = :post_id
        ORDER BY C."CommentID" DESC
        """)
        
        rows = session.execute(query, {"post_id": postid}).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        print("Error getting comments:", e)
        return []
    finally:
        session.close()
    
def getWatchedTitles(userid: int) -> list:
    """Return titles of TV/movies the user has watched"""
    session = get_session()
    try:
        query = text("""
            SELECT T."Title"
            FROM "watched" W
            JOIN "tvmovie" T ON W."MediaID" = T."MediaID"
            WHERE W."UserID" = :user_id;
        """)
        rows = session.execute(query, {"user_id": userid}).scalars().all()
        return rows
    except Exception as e:
        print("Error getting watched titles:", e)
        return []
    finally:
        session.close()


def addToWatched(user_id, title):
    """Add a show to the user's watched list using SQLAlchemy only."""
    session = get_session()
    try:
        result = session.execute(text('SELECT "MediaID" FROM "tvmovie" WHERE "Title" = :title'),{"title": title}).scalar()   

        if result is None:
            media_id = session.execute(text('INSERT INTO "tvmovie" ("Title") VALUES (:title) RETURNING "MediaID"'),{"title": title}).scalar()
        else:
            media_id = result
        session.execute(
            text("""
                INSERT INTO "watched" ("UserID", "MediaID")
                VALUES (:user_id, :media_id)
                ON CONFLICT DO NOTHING;
            """),
            {"user_id": user_id, "media_id": media_id}
        )
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error adding to watched list:", e)
        return False
    finally:
        session.close()

def removeFromWatched(user_id, title):
    """Remove a show from the user's watched list."""
    session = get_session()
    try:
        media_id = session.execute(text('SELECT "MediaID" FROM "tvmovie" WHERE "Title" = :title'),{"title": title}).scalar()

        if media_id is not None:
            session.execute(text('DELETE FROM "watched" WHERE "UserID" = :user_id AND "MediaID" = :media_id'),{"user_id": user_id, "media_id": media_id})
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print("Error removing from watched:", e)
        return False
    finally:
        session.close()

def getWatchingTitles(userid: int) -> list:
    """Return titles of TV/movies the user is currently watching"""
    session = get_session()
    try:
        query = text("""
            SELECT T."Title"
            FROM "watching" W
            JOIN "tvmovie" T ON W."MediaID" = T."MediaID"
            WHERE W."UserID" = :user_id;
        """)
        rows = session.execute(query, {"user_id": userid}).scalars().all()
        return rows
    except Exception as e:
        print("Error getting watching titles:", e)
        return []
    finally:
        session.close()
    
def addToCurrentlyWatching(user_id, title):
    """Add a show to the user's currently watching list using SQLAlchemy only."""
    session = get_session()
    try:
        result = session.execute(text('SELECT "MediaID" FROM "tvmovie" WHERE "Title" = :title'),{"title": title}).scalar()

        if result is None:
            media_id = session.execute(text('INSERT INTO "tvmovie" ("Title") VALUES (:title) RETURNING "MediaID"'),{"title": title}).scalar()
        else:
            media_id = result

        session.execute(
            text("""
                INSERT INTO "watching" ("UserID", "MediaID")
                VALUES (:user_id, :media_id)
                ON CONFLICT DO NOTHING;
            """),
            {"user_id": user_id, "media_id": media_id}
        )

        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error adding to currently watching list:", e)
        return False
    finally:
        session.close()

def removeFromCurrentlyWatching(user_id, title):
    """Remove a show from the user's currently watching list."""
    session = get_session()
    try:
        media_id = session.execute(text('SELECT "MediaID" FROM "tvmovie" WHERE "Title" = :title'),{"title": title}).scalar()

        if media_id is not None:
            session.execute(text('DELETE FROM "watching" WHERE "UserID" = :user_id AND "MediaID" = :media_id'),{"user_id": user_id, "media_id": media_id})
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print("Error removing from currently watching:", e)
        return False
    finally:
        session.close()


def getWatchlistTitles(userid: int) -> list:
    """Return titles of TV/movies the user has in their watchlist"""
    session = get_session()
    try:
        query = text("""
            SELECT T."Title"
            FROM "watchlist" W
            JOIN "tvmovie" T ON W."MediaID" = T."MediaID"
            WHERE W."UserID" = :user_id;
        """)
        rows = session.execute(query, {"user_id": userid}).scalars().all()
        return rows
    except Exception as e:
        print("Error getting watchlist titles:", e)
        return []
    finally:
        session.close()

def addToWatchlist(user_id, title):
    """Add a show to the user's watchlist using SQLAlchemy only."""
    session = get_session()
    try:
        result = session.execute(text('SELECT "MediaID" FROM "tvmovie" WHERE "Title" = :title'),{"title": title}).scalar()

        if result is None:
            media_id = session.execute(text('INSERT INTO "tvmovie" ("Title") VALUES (:title) RETURNING "MediaID"'),{"title": title}).scalar()
        else:
            media_id = result

        session.execute(
            text("""
                INSERT INTO "watchlist" ("UserID", "MediaID")
                VALUES (:user_id, :media_id)
                ON CONFLICT DO NOTHING;
            """),
            {"user_id": user_id, "media_id": media_id}
        )

        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error adding to watchlist:", e)
        return False
    finally:
        session.close()

def removeFromWatchlist(user_id, title):
    """Remove a show from the user's watchlist."""
    session = get_session()
    try:
        media_id = session.execute(text('SELECT "MediaID" FROM "tvmovie" WHERE "Title" = :title'),{"title": title}).scalar()

        if media_id is not None:
            session.execute(text('DELETE FROM "watchlist" WHERE "UserID" = :user_id AND "MediaID" = :media_id'),{"user_id": user_id, "media_id": media_id})
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print("Error removing from watchlist:", e)
        return False
    finally:
        session.close()

