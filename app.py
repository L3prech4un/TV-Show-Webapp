"""app.py: render and route to webpages"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from db.query import (get_all, insert, get_User, getFeed, getPostComments, getWatchedTitles, getWatchingTitles, 
                      getWatchlistTitles, createPost, addComment, deletePost, get_all_users_except_current, follow_user,
                      unfollow_user, get_followers, get_following, is_following, addToCurrentlyWatching, addToWatched, addToWatchlist,
                      removeFromCurrentlyWatching, removeFromWatched, removeFromWatchlist)
from db.server import init_database
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

# load environment variables from .env
load_dotenv()

#create cache for the user
userCache = {}

# database connection - values set in .env
db_name = os.getenv('db_name')
db_owner = os.getenv('db_owner')
db_pass = os.getenv('db_pass')
db_url = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"

def create_app():
    """Create Flask application and connect to your DB"""
    # create flask app
    app = Flask(__name__, 
                template_folder=os.path.join(os.getcwd(), 'templates'), 
                static_folder=os.path.join(os.getcwd(), 'static'))
    
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

    # create a webpage based off of the html in templates/index.html
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def register():
        """Sign up page: enables users to sign up"""
        if request.method == 'POST':
            try:
                # Read form fields that match the User model column names
                user = User(FName=request.form['FName'],
                            LName=request.form['LName'],
                            UName=request.form['UName'],
                            Email=request.form['Email'],
                            PWord=request.form['PWord'])
                insert(user)
                return redirect(url_for('login'))
            except Exception as e:
                # Print the error for debugging and redirect back to signup
                print("Error inserting user: ", e)
                return redirect('/signup')
        elif request.method == 'GET':
            return render_template('signup.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Log in page: enables users to log in"""
        if request.method == 'POST':
            try:
                # Query User table for user that matches the Email and Password submitted in the form
                user = get_User(User, Email=request.form["Email"], PWord=request.form['PWord'])
                if user:
                    loggedinuser = str(user.UserID)
                    userCache[loggedinuser] = user
                    response = redirect(url_for('my_feed'))
                    response.set_cookie('userloggedin',loggedinuser)
                    return response
                else:
                    print("Login did not have right credentials")
                    return render_template('login.html')
            except Exception as e:
                print("Error finding user: ", e)
                return render_template('login.html')
        elif request.method == 'GET':
            return render_template('login.html')

    @app.route('/users')
    def users():
        """Users page: displays all users in the Users table"""
        all_users = get_all(User)
        
        return render_template('users.html', users=all_users)

    @app.route('/success')
    def success():
        """Success page: displayed upon successful login"""

        #TODO: Make Index Page Different if user is logged in
        return render_template('index.html') # <- CHANGE 'index.html' EVENTUALLY

    @app.route('/my_profile')
    def my_profile():
        """User Profile page: displays the current Users profile page"""
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))
        
        try:
            userid = user.UserID
            username = user.UName
            watched = getWatchedTitles(userid)
            watching = getWatchingTitles(userid)
            watchlist = getWatchlistTitles(userid)
            
            tvmovies = get_all(TVMovie)
            return render_template('my_profile.html', tvmovies=tvmovies, username=username,watched=watched, watching=watching, watchlist=watchlist)
        except Exception as e:
            print("Error loading profile page:", e)

    @app.route('/about')
    def about():
        """About page: Displays the about us section of the website"""
        return render_template('about.html')
    
    @app.route('/my_feed', methods=['GET', 'POST'])
    def my_feed():
        """Feed page, Shows posts from following and self"""
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))

        try:
            if request.method == 'POST':
                postid = request.form.get('postid')
                content = request.form.get('content')
                if postid and content:
                    addComment(user.UserID, postid, content)
                
                deletepostid = request.form.get('deletepostid')
                if deletepostid:
                        deletePost(deletepostid)
            posts = getFeed(user.UserID)
            return render_template('feed.html', posts=posts, getPostComments=getPostComments)
        except Exception as e:
            print("Error Getting Feed Page", e)
            return render_template('feed.html', posts=[])
    
    @app.route('/create_post', methods=['GET', 'POST'])
    def create_post():
        """Allows User to Create their own posts"""
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            userid = user.UserID
            title = request.form.get('title')
            content = request.form.get('content')
            mediaid = request.form.get('mediaid')
            try:
                createPost(userid,mediaid,title,content)
                return redirect(url_for('my_feed'))
            except Exception as e:
                print("Error Occured while creating post", e)
                return redirect('/create_post')

        tvmovies = get_all(TVMovie)
        return render_template('createpost.html', tvmovies=tvmovies)
    
    @app.route('/discover')
    def discover():
        """Discover page to find and follow other users"""
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))
        
        suggested_users = get_all_users_except_current(user.UserID)
        following = get_following(user.UserID)
        followers = get_followers(user.UserID)
        
        return render_template('discover.html', 
                             suggested_users=suggested_users,
                             following=following,
                             followers=followers)

    @app.route('/follow/<int:user_id>', methods=['POST'])
    def follow_user_route(user_id):
        """Follow a user"""
        current_user = checkUserLogin()
        if not current_user:
            return redirect(url_for('login'))
        
        success = follow_user(current_user.UserID, user_id)
        if success:
            return jsonify({'success': True, 'message': 'User followed successfully'})
        else:
            return jsonify({'success': False, 'message': 'Already following this user'})

    @app.route('/unfollow/<int:user_id>', methods=['POST'])
    def unfollow_user_route(user_id):
        """Unfollow a user"""
        current_user = checkUserLogin()
        if not current_user:
            return redirect(url_for('login'))
        
        success = unfollow_user(current_user.UserID, user_id)
        if success:
            return jsonify({'success': True, 'message': 'User unfollowed successfully'})
        else:
            return jsonify({'success': False, 'message': 'Not following this user'})

    @app.route('/add_to_watched', methods=['POST'])
    def add_to_watched():
        """Add a TV show to the user's watched list"""
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))

        mediaid = request.form.get("mediaid")
        if not mediaid:
            return redirect(url_for('my_profile'))

        try:
            addToWatched(user.UserID, mediaid)
        except Exception as e:
            print("Error adding to watched:", e)

    
        return redirect(url_for('my_profile'))
    
    @app.route('/remove_from_watched', methods=['POST'])
    def remove_from_watched():
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))

        title = request.form.get("title")
        if not title:
            return redirect(url_for('my_profile'))

        try:
            removeFromWatched(user.UserID, title)
        except Exception as e:
            print("Error removing from watched:", e)

        return redirect(url_for('my_profile'))

    
    @app.route('/add_to_currently_watching', methods=['POST'])
    def add_to_currently_watching():
        """Add a TV show to the user's currently watching list"""
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))

        mediaid = request.form.get("mediaid")
        if not mediaid:
            return redirect(url_for('my_profile'))

        try:
            addToCurrentlyWatching(user.UserID, mediaid)
        except Exception as e:
            print("Error adding to currently watching:", e)

        return redirect(url_for('my_profile'))
    
    @app.route('/remove_from_currently_watching', methods=['POST'])
    def remove_from_currently_watching():
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))

        title = request.form.get("title")
        if not title:
            return redirect(url_for('my_profile'))

        try:
            removeFromCurrentlyWatching(user.UserID, title)
        except Exception as e:
            print("Error removing from currently watching:", e)

        return redirect(url_for('my_profile'))
    
    @app.route('/add_to_watchlist', methods=['POST'])
    def add_to_watchlist():
        """Add a TV show to the user's watchlist"""
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))

        mediaid = request.form.get("mediaid")
        if not mediaid:
            return redirect(url_for('my_profile'))

        try:
            addToWatchlist(user.UserID, mediaid)
        except Exception as e:
            print("Error adding to watchlist:", e)

        return redirect(url_for('my_profile'))
    
    @app.route('/remove_from_watchlist', methods=['POST'])
    def remove_from_watchlist():
        user = checkUserLogin()
        if not user:
            return redirect(url_for('login'))

        title = request.form.get("title")
        if not title:
            return redirect(url_for('my_profile'))

        try:
            removeFromWatchlist(user.UserID, title)
        except Exception as e:
            print("Error removing from watchlist:", e)

        return redirect(url_for('my_profile'))
    
    def checkUserLogin():
        """Check if the User is logged in"""
        loggedinuser = request.cookies.get('userloggedin')
        return userCache.get(loggedinuser)
    
    return app
    
if __name__ == "__main__":
    app = create_app()
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)