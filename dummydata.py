"""dummy_data.py: populate the TV-SHOW-WEBAPP database with sample data"""
from db.server import get_session
from db.schema.user import User
from db.schema.post import Post
from db.schema.comment import Comment
from db.schema.tvmovie import TVMovie
from db.schema.watched import Watched
from db.schema.watching import Watching
from db.schema.watchlist import Watchlist
from db.schema.creates import Creates
from db.schema.makes import Makes
from db.schema.follows import Follows

from sqlalchemy import insert

def create_dummy_data():
    session = get_session()

    # --- USERS ---
    user1 = User(FName="Alice", LName="Smith", UName="alice123", PWord="pass123", Email="alice@example.com")
    user2 = User(FName="Bob", LName="Jones", UName="bobby", PWord="secret", Email="bob@example.com")
    user3 = User(FName="Charlie", LName="Brown", UName="charlieB", PWord="choco", Email="charlie@example.com")

    session.add_all([user1, user2, user3])
    session.commit()

    # --- TV SHOWS / MOVIES ---
    movie1 = TVMovie(Title="Breaking Bad", Genre="Drama", Year="2008", Type="TV Show")
    movie2 = TVMovie(Title="Inception", Genre="Sci-Fi", Year="2010", Type="Movie")
    movie3 = TVMovie(Title="Friends", Genre="Comedy", Year="1994", Type="TV Show")

    session.add_all([movie1, movie2, movie3])
    session.commit()

    # --- POSTS ---
    post1 = Post(Title="Amazing Episode!", Date="2025-10-01", Content="Loved the ending!", MediaID=movie1.MediaID)
    post2 = Post(Title="Mind-bending Movie", Date="2025-10-05", Content="Inception blew my mind!", MediaID=movie2.MediaID)
    post3 = Post(Title="Classic Show", Date="2025-10-10", Content="Friends never gets old.", MediaID=movie3.MediaID)

    session.add_all([post1, post2, post3])
    session.commit()

    # --- COMMENTS ---
    comment1 = Comment(PostID=post1.PostID, Date="2025-10-02", Content="I agree, best episode yet!")
    comment2 = Comment(PostID=post2.PostID, Date="2025-10-06", Content="The ending confused me.")
    comment3 = Comment(PostID=post3.PostID, Date="2025-10-11", Content="Still watching reruns!")

    session.add_all([comment1, comment2, comment3])
    session.commit()

    # --- ASSOCIATIONS ---
    # Creates (user -> post)
    session.execute(insert(Creates).values([
        {"UserID": user1.UserID, "PostID": post1.PostID},
        {"UserID": user2.UserID, "PostID": post2.PostID},
        {"UserID": user3.UserID, "PostID": post3.PostID},
    ]))

    # Makes (user -> comment)
    session.execute(insert(Makes).values([
        {"UserID": user2.UserID, "CommentID": comment1.CommentID},
        {"UserID": user3.UserID, "CommentID": comment2.CommentID},
        {"UserID": user1.UserID, "CommentID": comment3.CommentID},
    ]))

    # Follows (user -> user)
    session.execute(insert(Follows).values([
        {"UserID": user1.UserID, "FollowerID": user2.UserID},
        {"UserID": user1.UserID, "FollowerID": user3.UserID},
        {"UserID": user2.UserID, "FollowerID": user3.UserID},
    ]))

    # Watched / Watching / Watchlist
    session.execute(insert(Watched).values([
        {"UserID": user1.UserID, "MediaID": movie1.MediaID},
        {"UserID": user2.UserID, "MediaID": movie2.MediaID},
    ]))

    session.execute(insert(Watching).values([
        {"UserID": user3.UserID, "MediaID": movie3.MediaID},
    ]))

    session.execute(insert(Watchlist).values([
        {"UserID": user1.UserID, "MediaID": movie2.MediaID},
        {"UserID": user2.UserID, "MediaID": movie3.MediaID},
    ]))

    session.commit()
    session.close()
    print("✅ Dummy data inserted successfully!")

if __name__ == "__main__":
    create_dummy_data()
