API Reference
=============

Database Query Functions
------------------------

All database operations are handled through `db/query.py`. Key functions:

.. py:function:: get_User(table, **filters)

   Get a single user by filters.

   :param table: Database table object
   :param **filters: Keyword arguments for filtering
   :return: User object or None

.. py:function:: get_all(table)

   Get all records from a table.

   :param table: Database table object
   :return: List of records

.. py:function:: getFeed(userid)

   Get feed posts for a user (posts from followed users + own posts).

   :param userid: User ID
   :return: List of post dictionaries

.. py:function:: createPost(userid, mediaid, title, content)

   Create a new post.

   :param userid: User ID creating the post
   :param mediaid: Media ID the post is about
   :param title: Post title
   :param content: Post content
   :return: None

.. py:function:: follow_user(user_id, follower_id)

   Follow another user.

   :param user_id: Current user ID
   :param follower_id: User ID to follow
   :return: Boolean indicating success

Database Models
---------------

**User Model** (`db/schema/user.py`):
   - UserID (Primary Key)
   - FName, LName, UName
   - Email, PWord (hashed)
   - Relationships: Post, Comment, TVMovie associations

**Post Model** (`db/schema/post.py`):
   - PostID (Primary Key)
   - MediaID (Foreign Key to TVMovie)
   - Title, Date, Content
   - Relationships: User, Comment, TVMovie

Flask Routes
------------

Main routes in `app.py`:

.. http:get:: /

   Home page.

.. http:get:: /login
.. http:post:: /login

   User login.

.. http:get:: /signup
.. http:post:: /signup

   User registration.

.. http:get:: /my_feed

   User's social feed.

.. http:get:: /discover

   Discover other users.

.. http:get:: /my_profile

   User profile page.

.. http:post:: /follow/<int:user_id>

   Follow a user (API endpoint).

.. http:post:: /search_users

   Search for users.