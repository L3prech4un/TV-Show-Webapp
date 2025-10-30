"""app.py: render and route to webpages"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from db.query import get_all, insert, get_User, changePost, deletePost, getFeed, getPostComments, getWatchedTitles, getWatchingTitles, getWatchlistTitles
from db.server import init_database, get_session
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
from datetime import datetime

# load environment variables from .env
load_dotenv()

userCache = {}

# database connection - values set in .env
db_name = os.getenv('db_name')
db_owner = os.getenv('db_owner')
db_pass = os.getenv('db_pass')
db_url = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"


def create_app():
    """Create Flask application and connect to your DB"""
    app = Flask(__name__,
                template_folder=os.path.join(os.getcwd(), 'templates'),
                static_folder=os.path.join(os.getcwd(), 'static'))

    app.secret_key = os.getenv('SECRET_KEY', 'dev_secret_key')  # Needed for session cookies

    # connect to db
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    # Initialize database
    with app.app_context():
        if not init_database():
            print("Failed to initialize database. Exiting.")
            exit(1)

    # ===============================================================
    # routes
    # ===============================================================

    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def register():
        """Sign up page"""
        if request.method == 'POST':
            try:
                user = User(
                    FName=request.form['FName'],
                    LName=request.form['LName'],
                    UName=request.form['UName'],
                    Email=request.form['Email'],
                    PWord=request.form['PWord']
                )
                insert(user)
                return redirect(url_for('login'))
            except Exception as e:
                print("Error inserting user:", e)
                return redirect('/signup')
        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Log in page"""
        if request.method == 'POST':
            try:
                user = get_User(User, Email=request.form["Email"], PWord=request.form['PWord'])
                if user:
                    token = str(user.UserID)
                    userCache[token] = user
                    session['token'] = token
                    session['user_id'] = user.UserID
                    resp = redirect(url_for('my_feed'))
                    resp.set_cookie('userToken', token)
                    return resp
                else:
                    print("Login failed: invalid credentials")
            except Exception as e:
                print("Error finding user:", e)
        return render_template('login.html')

    @app.route('/my_profile')
    def my_profile():
        """User Profile page"""
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))

        user = get_User(User, UserID=user_id)
        username = user.UName if user else "Guest"

        watched = getWatchedTitles(user_id)
        watching = getWatchingTitles(user_id)
        watchlist = getWatchlistTitles(user_id)

        return render_template('my_profile.html', username=username,watched=watched, watching=watching, watchlist=watchlist)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/my_feed', methods=['GET', 'POST'])
    def my_feed():
        """User Feed page"""
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))

        try:
            posts = getFeed(user.UserID)
            return render_template('feed.html', posts=posts, getPostComments=getPostComments)
        except Exception as e:
            print("Error in my_feed:", e)
            return render_template('feed.html', posts=[])

    @app.route('/add_comment/<int:post_id>', methods=['POST'])
    def add_comment(post_id):
        """Handle comment submission"""
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))

        content = request.form.get('content')
        if not content:
            return redirect(url_for('my_feed'))

        db_session = get_session()
        try:
            comment = Comment(PostID=post_id, Content=content)
            db_session.add(comment)
            db_session.flush()

            db_session.execute(Makes.insert().values(UserID=user.UserID, CommentID=comment.CommentID))
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            print("Error adding comment:", e)
        finally:
            db_session.close()

        return redirect(url_for('my_feed'))

    @app.route('/create_post', methods=['GET', 'POST'])
    def create_post():
        """Create new post"""
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))

        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            media_id = request.form.get('media_id')

            if not all([title, content, media_id]):
                return redirect(url_for('create_post'))

            db_session = get_session()
            try:
                post = Post(
                    Title=title,
                    Content=content,
                    Date=datetime.now().strftime("%Y-%m-%d"),
                    MediaID=media_id
                )
                db_session.add(post)
                db_session.flush()

                db_session.execute(Creates.insert().values(UserID=user.UserID, PostID=post.PostID))
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                print("Error creating post:", e)
            finally:
                db_session.close()

            return redirect(url_for('my_feed'))

        tvmovies = get_all(TVMovie)
        return render_template('createpost.html', tvmovies=tvmovies)
    
    @app.route('/delete_post/<int:post_id>', methods=['POST'])
    def delete_post(post_id):
        """Delete a post if the logged-in user created it"""
        user = checkUserLogin()
        if not user:
            return redirect(url_for('my_feed'))

        try:
            success = deletePost(user.UserID, post_id)
            if not success:
                print(f"User {user.UserID} not authorized or post not found.")
        except Exception as e:
            print("Error deleting post:", e)

        return redirect(url_for('my_feed'))

    return app


def checkUserLogin():
    """Check if user is logged in via session token"""
    token = session.get('token')
    return userCache.get(token)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
