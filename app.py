"""app.py: render and route to webpages"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from db.query import get_all, insert, get_User
from db.server import init_database
# from db.schema.comment import Comment
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
                    return redirect(url_for('success'))
            except Exception as e:
                print("Error finding user: ", e)
                return redirect('/login')
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
        #TODO: User cookies to only render my_profile.html if the user is logged in otherwise, this should take them to the login page -Matt
        return render_template('my_profile.html')

    @app.route('/about')
    def about():
        """About page: Displays the about us section of the website"""
        return render_template('about.html')
    
    @app.route('/my_feed')
    def my_feed():
        """User feed page: Shows posts from following or random"""
        #TODO: Implement cookies to 
        return render_template('feed.html')

    return app

if __name__ == "__main__":
    app = create_app()
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)