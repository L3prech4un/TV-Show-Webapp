Database Schema
===============

Entity Relationship Diagram
---------------------------

::

   User ───┐
           ├── Creates ─── Post ─── TVMovie
           ├── Makes ───── Comment
           ├── Follows ─── User (self-referential)
           ├── Watched ─── TVMovie
           ├── Watching ── TVMovie
           └── Watchlist ─ TVMovie

Table Descriptions
------------------

**Users Table**
^^^^^^^^^^^^^^^

.. code-block:: sql

   CREATE TABLE user (
       UserID SERIAL PRIMARY KEY,
       FName VARCHAR(40),
       LName VARCHAR(40),
       UName VARCHAR(40),
       PWord VARCHAR(100),
       Email VARCHAR(40)
   );

**Posts Table**
^^^^^^^^^^^^^^^

.. code-block:: sql

   CREATE TABLE post (
       PostID SERIAL PRIMARY KEY,
       MediaID INTEGER REFERENCES tvmovie(MediaID),
       Title VARCHAR(40),
       Date VARCHAR(40),
       Content VARCHAR(40)
   );

**TVMovie Table**
^^^^^^^^^^^^^^^^^

.. code-block:: sql

   CREATE TABLE tvmovie (
       MediaID INTEGER PRIMARY KEY,
       Title VARCHAR(40),
       Genre VARCHAR(40),
       Year VARCHAR(40),
       Type VARCHAR(40)
   );

Association Tables
------------------

The application uses several association tables for many-to-many relationships:

1. **creates**: Links users to their posts
2. **makes**: Links users to their comments
3. **follows**: Links users to other users (follow relationships)
4. **watched/watching/watchlist**: Links users to media in different categories

Sample Queries
--------------

Get a user's feed:

.. code-block:: sql

   SELECT posts.*, users.UName
   FROM posts
   JOIN creates ON posts.PostID = creates.PostID
   JOIN users ON creates.UserID = users.UserID
   WHERE users.UserID IN (
       SELECT FollowerID FROM follows WHERE UserID = :current_user_id
   ) OR users.UserID = :current_user_id
   ORDER BY posts.Date DESC;

Get users a user is following:

.. code-block:: sql

   SELECT u.*
   FROM users u
   JOIN follows f ON u.UserID = f.FollowerID
   WHERE f.UserID = :current_user_id;