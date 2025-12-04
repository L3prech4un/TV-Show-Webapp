Development Guide
=================

Project Structure
-----------------

::

   TV-Show-Webapp/
   ├── app.py                    # Main Flask application
   ├── requirements.txt          # Python dependencies
   ├── Dockerfile               # Container configuration
   ├── docker-compose.yml       # Multi-container setup
   ├── .env                     # Environment variables (create this)
   │
   ├── db/                      # Database layer
   │   ├── server.py           # Database connection
   │   ├── query.py            # Database queries
   │   └── schema/             # SQLAlchemy models
   │       ├── __init__.py
   │       ├── user.py
   │       ├── post.py
   │       └── ...
   │
   ├── static/                  # Static files (CSS, images)
   │   ├── images/
   │   └── *.css files
   │
   ├── templates/               # HTML templates
   │   ├── index.html
   │   ├── login.html
   │   └── ...
   │
   ├── docs/                    # Documentation (you are here!)
   │   ├── conf.py
   │   ├── index.rst
   │   └── *.rst files
   │
   └── logs/                    # Application logs

Setting Up Development Environment
----------------------------------

1. Clone the repository
2. Set up virtual environment
3. Install development dependencies:

   .. code-block:: bash

      pip install -r requirements.txt
      pip install pytest pytest-flask  # For testing

Database Schema
---------------

The application uses PostgreSQL with SQLAlchemy ORM. Key tables:

* **User**: User accounts and profiles
* **Post**: User-created posts about media
* **Comment**: Comments on posts
* **TVMovie**: Media information (TV shows and movies)
* **Follows**: User follow relationships
* **Watched/Watching/Watchlist**: User-media relationships

Running in Development Mode
---------------------------

.. code-block:: bash

   # Set Flask to development mode
   export FLASK_ENV=development  # Mac/Linux
   set FLASK_ENV=development     # Windows

   # Run with debug mode
   python app.py

   # Or use Flask CLI
   flask run --debug

Testing
-------

The application includes logging but no formal tests. To add tests:

1. Create a `tests/` directory
2. Write tests using pytest
3. Run tests with: `pytest tests/`

Code Style Guidelines
---------------------

* Follow PEP 8 for Python code
* Use meaningful variable and function names
* Add docstrings to all functions and classes
* Keep functions focused on single responsibilities

Common Development Tasks
------------------------

**Adding a New Feature:**

1. Create database models in `db/schema/`
2. Add queries in `db/query.py`
3. Create routes in `app.py`
4. Add templates in `templates/`
5. Style with CSS in `static/`

**Debugging Tips:**

* Check `logs/log.txt` for errors
* Use Flask's debugger (when FLASK_ENV=development)
* Test database queries directly using Python shell

Future Improvements
-------------------

Potential enhancements for the project:

1. Add user profile pictures
2. Implement likes/reactions on posts
3. Add notifications system
4. Create mobile-responsive design
5. Add email verification
6. Implement password reset functionality