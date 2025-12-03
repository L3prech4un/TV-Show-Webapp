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


def hash_password(password: str) -> str:
    """Hashes the password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_dummy_data():
    session = get_session()
    try:
        users = [
            User(FName="Alice", LName="Smith", UName="alice123", PWord=hash_password("pass123"), Email="alice@example.com"),
            User(FName="Bob", LName="Jones", UName="bobby", PWord=hash_password("secret"), Email="bob@example.com"),
            User(FName="Charlie", LName="Brown", UName="charlieB", PWord=hash_password("charlie123"), Email="charlie@example.com"),
            User(FName="Diana", LName="Prince", UName="dianaP", PWord=hash_password("wonder"), Email="diana@example.com"),
            User(FName="Eve", LName="Adams", UName="eveA", PWord=hash_password("evepass"), Email="eve@example.com")
        ]
        session.add_all(users)
        session.flush()

        shows = [
            TVMovie(Title="Stranger Things", Genre="Sci-Fi", Year="2016", Type="TV"),
            TVMovie(Title="The Matrix", Genre="Action", Year="1999", Type="Movie"),
            TVMovie(Title="Breaking Bad", Genre="Drama", Year="2008", Type="TV"),
            TVMovie(Title="The Witcher", Genre="Fantasy", Year="2019", Type="TV"),
            TVMovie(Title="Inception", Genre="Sci-Fi", Year="2010", Type="Movie")
        ]
        session.add_all(shows)
        session.flush()  

        posts = [
            Post(MediaID=shows[0].MediaID, Title="Love Stranger Things!", Date="2025-10-30", Content="Best show ever!", Spoiler=False, Rating=4),  
            Post(MediaID=shows[1].MediaID, Title="Matrix Review", Date="2025-10-29", Content="Classic movie", Spoiler=True, Rating=2),           
            Post(MediaID=shows[2].MediaID, Title="BB Thoughts", Date="2025-10-28", Content="Just finished Breaking Bad", Spoiler=True, Rating=1),  
            Post(MediaID=shows[3].MediaID, Title="Geralt Forever!", Date="2025-10-27", Content="The Witcher rocks!", Spoiler=False, Rating=3),    
            Post(MediaID=shows[4].MediaID, Title="Mind Blown!", Date="2025-10-26", Content="Inception is a masterpiece!", Spoiler=True, Rating=4) 
        ]
        session.add_all(posts)
        session.flush()  


        follows_data = [
            {"UserID": users[0].UserID, "FollowerID": users[1].UserID}, 
            {"UserID": users[1].UserID, "FollowerID": users[2].UserID}, 
            {"UserID": users[2].UserID, "FollowerID": users[0].UserID}, 
            {"UserID": users[3].UserID, "FollowerID": users[4].UserID},
            {"UserID": users[4].UserID, "FollowerID": users[3].UserID}, 
        ]
        session.execute(Follows.insert(), follows_data)

        creates_data = [
            {"UserID": users[0].UserID, "PostID": posts[0].PostID},
            {"UserID": users[1].UserID, "PostID": posts[1].PostID},
            {"UserID": users[2].UserID, "PostID": posts[2].PostID},
            {"UserID": users[3].UserID, "PostID": posts[3].PostID},
            {"UserID": users[4].UserID, "PostID": posts[4].PostID},
        ]
        session.execute(Creates.insert(), creates_data)

        comments = [
            Comment(PostID=posts[0].PostID, Content="Totally agree!"), 
            Comment(PostID=posts[1].PostID, Content="Need to rewatch"),  
            Comment(PostID=posts[2].PostID, Content="Best ending ever"),
            Comment(PostID=posts[3].PostID, Content="Geralt forever!"),
            Comment(PostID=posts[4].PostID, Content="Mind blown!") 
        ]
        session.add_all(comments)
        session.flush() 

        makes_data = [
            {"UserID": users[1].UserID, "CommentID": comments[0].CommentID},  
            {"UserID": users[2].UserID, "CommentID": comments[1].CommentID},    
            {"UserID": users[0].UserID, "CommentID": comments[2].CommentID},  
            {"UserID": users[4].UserID, "CommentID": comments[3].CommentID},  
            {"UserID": users[3].UserID, "CommentID": comments[4].CommentID} 
        ]
        session.execute(Makes.insert(), makes_data)

        watchlist_data = [
            {"UserID": users[0].UserID, "MediaID": shows[2].MediaID},
            {"UserID": users[1].UserID, "MediaID": shows[0].MediaID},
            {"UserID": users[2].UserID, "MediaID": shows[1].MediaID},
            {"UserID": users[3].UserID, "MediaID": shows[4].MediaID},
            {"UserID": users[4].UserID, "MediaID": shows[3].MediaID},
        ]
        session.execute(Watchlist.insert(), watchlist_data)

        watching_data = [
            {"UserID": users[0].UserID, "MediaID": shows[0].MediaID},
            {"UserID": users[1].UserID, "MediaID": shows[1].MediaID},
            {"UserID": users[2].UserID, "MediaID": shows[2].MediaID},
            {"UserID": users[3].UserID, "MediaID": shows[3].MediaID},
            {"UserID": users[4].UserID, "MediaID": shows[4].MediaID},
        ]
        session.execute(Watching.insert(), watching_data)

        watched_data = [
            {"UserID": users[0].UserID, "MediaID": shows[1].MediaID},
            {"UserID": users[1].UserID, "MediaID": shows[2].MediaID},
            {"UserID": users[2].UserID, "MediaID": shows[0].MediaID},
            {"UserID": users[3].UserID, "MediaID": shows[4].MediaID},
            {"UserID": users[4].UserID, "MediaID": shows[3].MediaID},
        ]
        session.commit()
        print("Successfully inserted dummy data with hashed passwords!")

    except Exception as e:
        session.rollback()
        print(f"Error inserting dummy data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    create_dummy_data()