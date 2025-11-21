"""app.py: render and route to webpages"""

import os
import bcrypt
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from db.server import init_database
import db.query as query
from db import schema

# load environment variables from .env
load_dotenv()

#create cache for the user
userCache = {}

# configure logging
logging.basicConfig(
    filename="logs/log.txt", level=logging.INFO, filemode="a", format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

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
        logger.info("User has accessed home page")
        return render_template('index.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def register():
        """Sign up page: enables users to sign up"""
        logger.info("User has accessed signup page")
        if request.method == 'POST':
            try:
                # get form data and sanitize
                firstName = request.form['FName'].strip()
                lastName = request.form['LName'].strip()
                userName = request.form['UName'].strip()
                email = request.form['Email'].strip()
                password = request.form['PWord'].strip()

                # validate first name
                if not firstName.isalpha() and len(firstName) >= 2:
                    error = "First name can only contain letters and must be at least two characters."
                    logger.warning(f"Invalid first name attempt: {firstName}")
                    return render_template('signup.html', error=error)
                
                # validate last name
                if not lastName.isalpha() and len(lastName) >= 2:
                    error = "Last name can only contain letters and must be at least two characters."
                    logger.warning(f"Invalid last name attempt: {lastName}")
                    return render_template('signup.html', error=error)
                
                # validate user name
                if not len(userName) >= 2:
                    error = "User name has to be at least two characters."
                    logger.warning(f"Invalid Username attempt: {error}")
                    return render_template('signup.html', error=error)
                
                # validate password
                if not len(password) >= 8:
                    error = "Password has to be at least eight characters."
                    logger.warning(f"Invalid password attempt: {error}")
                    return render_template('signup.html', error=error)
                
                # hash and salt password 
                salt = bcrypt.gensalt()
                hashedPassword = bcrypt.hashpw(password.encode('utf-8'), salt)

                # create a user object with form info
                user = schema.User(FName=firstName,
                            LName=lastName,
                            UName=userName,
                            Email=email,
                            PWord=hashedPassword.decode('utf8'))
                
                # insert the user into the database
                query.insert(user)

                # go to login page
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
        logger.info("User has accessed login page")
        if request.method == 'POST':
            try:
                # get the email and password from the login form
                password = request.form['PWord']
                email = request.form['Email']

                # query for the existence of a user with that email
                user = query.get_User(schema.User, Email=email)

                # create a default error message for security sake
                error = f"failed login attempt for: {email}"

                if not user:
                    logger.warning(f"Login attempt with non-existent email: {email}")
                    return render_template('login.html', error=error)
                
                if bcrypt.checkpw(password.encode('utf-8'), user.PWord.encode('utf-8')):
                    logger.info(f"Successful login: {email}")
                    loggedinuser = str(user.UserID)
                    userCache[loggedinuser] = user
                    response = redirect(url_for('my_feed'))
                    response.set_cookie('userloggedin', loggedinuser)
                    return response
                
                else:
                    logger.warning(f"Login attempted with incorrect password")
                    return render_template('login.html', error=error)
                
            except Exception as e:
                logger.error(f"An error occurred during login: {e}")
                return render_template('login.html')
        elif request.method == 'GET':
            return render_template('login.html')

    @app.route('/users')
    def users():
        """Users page: displays all users in the Users table"""
        all_users = query.get_all(schema.User)
        
        return render_template('users.html', users=all_users)

    @app.route('/success')
    def success():
        """Success page: displayed upon successful login"""

        #TODO: Make Index Page Different if user is logged in
        return render_template('index.html') # <- CHANGE 'index.html' EVENTUALLY

    @app.route('/my_profile')
    def my_profile():
        """User Profile page: displays the current Users profile page"""
        logger.info("User has accessed profile page")
        user = checkUserLogin()
        if not user:
            logger.warning("No User logged in")
            return redirect(url_for('login'))
        
        try:
            userid = user.UserID
            username = user.UName
            watched = query.getTitles(userid, "watched", "watched_title")
            watching = query.getTitles(userid, "watching", "watching_title")
            watchlist = query.getTitles(userid, "watchlist", "watchlist_title")
            
            tvmovies = query.get_all(schema.TVMovie)
            return render_template('my_profile.html', tvmovies=tvmovies, username=username, watched=watched, watching=watching, watchlist=watchlist)
        except Exception as e:
            logger.warning(f"Error loading profile page: {e}")

    @app.route('/about')
    def about():
        """About page: Displays the about us section of the website"""
        logger.info("User has accessed about page")
        return render_template('about.html')
    
    @app.route('/my_feed', methods=['GET', 'POST'])
    def my_feed():
        """Feed page, Shows posts from following and self"""
        logger.info("User has accessed feed page")
        user = checkUserLogin()
        if not user:
            logger.warning("No user logged in")
            return redirect(url_for('login'))

        try:
            if request.method == 'POST':
                postid = request.form.get('postid')
                content = request.form.get('content')
                if postid and content:
                    query.addComment(user.UserID, postid, content)
                    logger.info(f"Comment created on Post: {postid}")
                
                deletepostid = request.form.get('deletepostid')
                if deletepostid:
                    query.deletePost(deletepostid)
                    logger.info(f"Post has been Deleted: {deletepostid}")
            posts = query.getFeed(user.UserID)
            return render_template('feed.html', posts=posts, getPostComments=query.getPostComments)
        except Exception as e:
            logger.warning(f"Error Getting Feed Page: {e}")
            return render_template('feed.html', posts=[])
    
    @app.route('/create_post', methods=['GET', 'POST'])
    def create_post():
        """Allows User to Create their own posts"""
        logger.info("User has accessed create post page")
        user = checkUserLogin()
        if not user:
            logger.info("No User is logged in")
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            userid = user.UserID
            title = request.form.get('title')
            content = request.form.get('content')
            mediaid = request.form.get('mediaid')
            try:
                query.createPost(userid,mediaid,title,content)
                logger.info("User has succesfully created a post")
                return redirect(url_for('my_feed'))
            except Exception as e:
                logger.warning(f"Error Occurred while creating post {e}")
                return redirect('/create_post')

        tvmovies = query.get_all(schema.TVMovie)
        return render_template('createpost.html', tvmovies=tvmovies)
    
    @app.route('/discover')
    def discover():
        """Discover page to find and follow other users"""
        user = checkUserLogin()
        logger.info("User has accessed discover page")
        if not user:
            logger.warning("No User is logged in")
            return redirect(url_for('login'))
        
        suggested_users = query.get_all_users_except_current(user.UserID)
        following = query.get_following(user.UserID)
        followers = query.get_followers(user.UserID)
        
        return render_template('discover.html', 
                             suggested_users=suggested_users,
                             following=following,
                             followers=followers)

    @app.route('/follow/<int:user_id>', methods=['POST'])
    def follow_user_route(user_id):
        """Follow a user"""
        current_user = checkUserLogin()

        if not current_user:
            logger.warning("No User is logged in")
            return redirect(url_for('login'))
        
        success = query.follow_user(current_user.UserID, user_id)
        if success:
            logger.info("User has followed successfully")
            return jsonify({'success': True, 'message': 'User followed successfully'})
        else:
            logger.warning("User is already following other user")
            return jsonify({'success': False, 'message': 'Already following this user'})

    @app.route('/unfollow/<int:user_id>', methods=['POST'])
    def unfollow_user_route(user_id):
        """Unfollow a user"""
        current_user = checkUserLogin()
        if not current_user:
            logger.info("No User is logged in")
            return redirect(url_for('login'))
        
        success = query.unfollow_user(current_user.UserID, user_id)
        if success:
            logger.info("User has unfollowed successfully")
            return jsonify({'success': True, 'message': 'User unfollowed successfully'})
        else:
            logger.warning("User is not following this user")
            return jsonify({'success': False, 'message': 'Not following this user'})

    @app.route('/add_to_watched', methods=['POST'])
    def add_to_watched():
        """Add a movie/show to the user's watched list"""
        user = checkUserLogin()
        if not user:
            logger.warning("No user is logged in")
            return redirect(url_for('login'))

        mediaid = request.form.get("mediaid")
        if not mediaid:
            return redirect(url_for('my_profile'))

        try:
            query.addToWatchTable(user.UserID, mediaid, "watched")
            logger.info("User has successfully added media to watched")
        except Exception as e:
            logger.warning(f"Error adding to watched: {e}")

    
        return redirect(url_for('my_profile'))
    
    @app.route('/remove_from_watched', methods=['POST'])
    def remove_from_watched():
        """Remove a movie/show from a user's watched list"""
        user = checkUserLogin()
        if not user:
            logger.warning("No user is logged in")
            return redirect(url_for('login'))

        title = request.form.get("title")
        if not title:
            return redirect(url_for('my_profile'))

        try:
            query.removeFromWatchTable(user.UserID, title, "watched")
            logger.info("User has successfully removed media from watched")
        except Exception as e:
            logger.warning(f"Error removing from watched: {e}")

        return redirect(url_for('my_profile'))

    
    @app.route('/add_to_currently_watching', methods=['POST'])
    def add_to_currently_watching():
        """Add a movie/show to the user's currently watching list"""
        user = checkUserLogin()
        if not user:
            logger.warning("No User is logged in")
            return redirect(url_for('login'))

        mediaid = request.form.get("mediaid")
        if not mediaid:
            return redirect(url_for('my_profile'))

        try:
            query.addToWatchTable(user.UserID, mediaid, "watching")
            logger.info("User has successfully added media to watching")
        except Exception as e:
            logger.warning(f"Error adding to currently watching: {e}")

        return redirect(url_for('my_profile'))
    
    @app.route('/remove_from_currently_watching', methods=['POST'])
    def remove_from_currently_watching():
        """Remove movie/show from user's currently watching list"""
        user = checkUserLogin()
        if not user:
            logger.warning("No User is logged in")
            return redirect(url_for('login'))

        title = request.form.get("title")
        if not title:
            return redirect(url_for('my_profile'))

        try:
            query.removeFromWatchTable(user.UserID, title, "watching")
            logger.info("User has successfully removed media from watching")
        except Exception as e:
            logger.warning(f"Error removing from currently watching: {e}")

        return redirect(url_for('my_profile'))
    
    @app.route('/add_to_watchlist', methods=['POST'])
    def add_to_watchlist():
        """Add movie/show to the user's watchlist"""
        user = checkUserLogin()
        if not user:
            logger.warning("No User is logged in")
            return redirect(url_for('login'))

        mediaid = request.form.get("mediaid")
        if not mediaid:
            return redirect(url_for('my_profile'))

        try:
            query.addToWatchTable(user.UserID, mediaid, "watchlist")
            logger.info("User has successfully added media to watchlist")
        except Exception as e:
            logger.warning(f"Error adding to watchlist: {e}")

        return redirect(url_for('my_profile'))
    
    @app.route('/remove_from_watchlist', methods=['POST'])
    def remove_from_watchlist():
        """Remove movie/show from a user's watchlist"""
        user = checkUserLogin()
        if not user:
            logger.warning("No user is logged in")
            return redirect(url_for('login'))

        title = request.form.get("title")
        if not title:
            return redirect(url_for('my_profile'))

        try:
            query.removeFromWatchTable(user.UserID, title, "watchlist")
            logger.info("User successfully removed media from watchlist")
        except Exception as e:
            logger.warning(f"Error removing from watchlist: {e}")

        return redirect(url_for('my_profile'))
    
    def checkUserLogin():
        """Check if the User is logged in"""
        loggedinuser = request.cookies.get('userloggedin')
        return userCache.get(loggedinuser)

    @app.route('/delete_comment/<int:comment_id>', methods=['POST'])
    def delete_comment(comment_id):
        """Delete a comment from a post"""
        user = checkUserLogin()
        if not user:
            logger.warning("No User is Logged in")
            return redirect(url_for('login'))
        
        try:
            success = query.deleteComment(comment_id, user.UserID)
            if success:
                logger.info(f"Comment {comment_id} deleted successfully by user {user.UserID}")
            else:
                logger.warning(f"User {user.UserID} failed to delete comment {comment_id}")
        except Exception as e:
            logger.error(f"Error deleting comment {comment_id}: {e}")
        
        return redirect(url_for('my_feed'))

    return app
    
if __name__ == "__main__":
    app = create_app()
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)