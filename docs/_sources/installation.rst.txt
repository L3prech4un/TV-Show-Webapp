Installation Guide
==================

Prerequisites
-------------

Before installing TV-Show-Webapp, make sure you have:

* Python 3.11 or higher
* PostgreSQL 15 or higher
* Docker and Docker Compose (optional, for containerized deployment)
* Git (for cloning the repository)

Step 1: Clone the Repository
----------------------------

.. code-block:: bash

   git clone https://github.com/L3prech4un/TV-Show-Webapp.git
   cd TV-Show-Webapp

Step 2: Set Up Virtual Environment
----------------------------------

.. code-block:: bash

   # Create virtual environment
   python -m venv venv
   
   # Activate it
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate

Step 3: Install Dependencies
----------------------------

.. code-block:: bash

   pip install -r requirements.txt

Step 4: Configure Environment Variables
---------------------------------------

Create a `.env` file in the project root:

.. code-block:: bash

   # Database configuration
   db_host=localhost
   db_port=5432
   db_name=TV-Show-Webapp
   db_owner=postgres
   db_pass=your_password_here

Step 5: Set Up Database
-----------------------

.. code-block:: bash

   # Using Docker (recommended):
   docker-compose up -d db
   
   # Or manually create PostgreSQL database:
   # 1. Start PostgreSQL service
   # 2. Create database: CREATE DATABASE tvshow_webapp;
   # 3. Run: python dummydata.py (optional, for test data)

Step 6: Run the Application
---------------------------

.. code-block:: bash

   # Option 1: Using Docker Compose
   docker-compose up
   
   # Option 2: Run Flask directly
   python app.py

   # The app will be available at http://localhost:5000

Troubleshooting Installation
----------------------------

* **Port 5432 already in use**: Change `db_port` in `.env` to another port (e.g., 5433)
* **Database connection errors**: Verify PostgreSQL is running and credentials are correct
* **Module not found errors**: Make sure virtual environment is activated and all packages are installed