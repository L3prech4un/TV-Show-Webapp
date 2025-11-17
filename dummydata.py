"""dummydata.py: populate all tables in TV-SHOW-WEBAPP database respecting feed visibility"""

import bcrypt
from db.server import get_session
from db.schema.user import User
from db.schema.post import Post
from db.schema.comment import Comment
from db.schema.tvmovie import TVMovie
from db.schema.creates import Creates
from db.schema.follows import Follows
from db.schema.makes import Makes
from db.schema.watched import Watched
from db.schema.watching import Watching
from db.schema.watchlist import Watchlist

def hashPasswords(password: str) -> str:
    """Return Hashed version of password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_dummy_data():    
    session = get_session()
    try:
        # --- Create Users ---
        users = [
            User(FName="Alice", LName="Smith", UName="alice123", PWord=hashPasswords("password123"), Email="alice@example.com"),
            User(FName="Bob", LName="Jones", UName="bobby", PWord=hashPasswords("secret123"), Email="bob@example.com"),
            User(FName="Charlie", LName="Brown", UName="charlieB", PWord=hashPasswords("charlie123"), Email="charlie@example.com"),
            User(FName="Diana", LName="Prince", UName="dianaP", PWord=hashPasswords("wonder123"), Email="diana@example.com"),
            User(FName="Eve", LName="Adams", UName="eveA", PWord=hashPasswords("evepass123"), Email="eve@example.com")
        ]
        session.add_all(users)
        session.flush()  # Assigns UserIDs

        # --- Create TV Shows and Movies ---
        shows = [
            TVMovie(Title="Stranger Things", Genre="Sci-Fi", Year="2016", Type="TV"),
            TVMovie(Title="The Matrix", Genre="Action", Year="1999", Type="Movie"),
            TVMovie(Title="Breaking Bad", Genre="Drama", Year="2008", Type="TV"),
            TVMovie(Title="The Witcher", Genre="Fantasy", Year="2019", Type="TV"),
            TVMovie(Title="Inception", Genre="Sci-Fi", Year="2010", Type="Movie")
        ]
        session.add_all(shows)
        session.flush()  # Assigns MediaIDs

        # --- Create Posts ---
        posts = [
            Post(MediaID=shows[0].MediaID, Title="Love Stranger Things!", Date="2025-10-30", Content="Best show ever!"),  # Alice
            Post(MediaID=shows[1].MediaID, Title="Matrix Review", Date="2025-10-29", Content="Classic movie"),            # Bob
            Post(MediaID=shows[2].MediaID, Title="BB Thoughts", Date="2025-10-28", Content="Just finished Breaking Bad"),  # Charlie
            Post(MediaID=shows[3].MediaID, Title="Geralt Forever!", Date="2025-10-27", Content="The Witcher rocks!"),     # Diana
            Post(MediaID=shows[4].MediaID, Title="Mind Blown!", Date="2025-10-26", Content="Inception is a masterpiece!") # Eve
        ]
        session.add_all(posts)
        session.flush()  # Assigns PostIDs

        # --- Create Follows Relationships ---
        follows_data = [
            {"UserID": users[0].UserID, "FollowerID": users[1].UserID},  # Alice follows Bob
            {"UserID": users[1].UserID, "FollowerID": users[2].UserID},  # Bob follows Charlie
            {"UserID": users[2].UserID, "FollowerID": users[0].UserID},  # Charlie follows Alice
            {"UserID": users[3].UserID, "FollowerID": users[4].UserID},  # Diana follows Eve
            {"UserID": users[4].UserID, "FollowerID": users[3].UserID},  # Eve follows Diana
        ]
        session.execute(Follows.insert(), follows_data)

        # --- Link Users to Posts (Creates) ---
        creates_data = [
            {"UserID": users[0].UserID, "PostID": posts[0].PostID},
            {"UserID": users[1].UserID, "PostID": posts[1].PostID},
            {"UserID": users[2].UserID, "PostID": posts[2].PostID},
            {"UserID": users[3].UserID, "PostID": posts[3].PostID},
            {"UserID": users[4].UserID, "PostID": posts[4].PostID},
        ]
        session.execute(Creates.insert(), creates_data)

        # --- Create Comments (respect visibility rules) ---
        comments = [
            Comment(PostID=posts[0].PostID, Content="Totally agree!"),   # Alice's post
            Comment(PostID=posts[1].PostID, Content="Need to rewatch"),  # Bob's post
            Comment(PostID=posts[2].PostID, Content="Best ending ever"), # Charlie's post
            Comment(PostID=posts[3].PostID, Content="Geralt forever!"),  # Diana's post
            Comment(PostID=posts[4].PostID, Content="Mind blown!")       # Eve's post
        ]
        session.add_all(comments)
        session.flush()  # Assign CommentIDs

        # --- Link Users to Comments (Makes) respecting visibility ---
        makes_data = [
            {"UserID": users[1].UserID, "CommentID": comments[0].CommentID},  # Bob can comment on Alice
            {"UserID": users[2].UserID, "CommentID": comments[1].CommentID},  # Charlie can comment on Bob
            {"UserID": users[0].UserID, "CommentID": comments[2].CommentID},  # Alice can comment on Charlie
            {"UserID": users[4].UserID, "CommentID": comments[3].CommentID},  # Eve can comment on Diana
            {"UserID": users[3].UserID, "CommentID": comments[4].CommentID}   # Diana can comment on Eve
        ]
        session.execute(Makes.insert(), makes_data)

        # --- Add Shows to Watchlist ---
        watchlist_data = [
            {"UserID": users[0].UserID, "MediaID": shows[2].MediaID},
            {"UserID": users[1].UserID, "MediaID": shows[0].MediaID},
            {"UserID": users[2].UserID, "MediaID": shows[1].MediaID},
            {"UserID": users[3].UserID, "MediaID": shows[4].MediaID},
            {"UserID": users[4].UserID, "MediaID": shows[3].MediaID},
        ]
        session.execute(Watchlist.insert(), watchlist_data)

        # --- Add Shows to Currently Watching ---
        watching_data = [
            {"UserID": users[0].UserID, "MediaID": shows[0].MediaID},
            {"UserID": users[1].UserID, "MediaID": shows[1].MediaID},
            {"UserID": users[2].UserID, "MediaID": shows[2].MediaID},
            {"UserID": users[3].UserID, "MediaID": shows[3].MediaID},
            {"UserID": users[4].UserID, "MediaID": shows[4].MediaID},
        ]
        session.execute(Watching.insert(), watching_data)

        # --- Add Shows to Watched List ---
        watched_data = [
            {"UserID": users[0].UserID, "MediaID": shows[1].MediaID},
            {"UserID": users[1].UserID, "MediaID": shows[2].MediaID},
            {"UserID": users[2].UserID, "MediaID": shows[0].MediaID},
            {"UserID": users[3].UserID, "MediaID": shows[4].MediaID},
            {"UserID": users[4].UserID, "MediaID": shows[3].MediaID},
        ]
        session.execute(Watched.insert(), watched_data)

        session.commit()
        print("Successfully inserted dummy data into all tables with feed visibility enforced!")

    except Exception as e:
        session.rollback()
        print("Error inserting dummy data:", e)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    create_dummy_data()