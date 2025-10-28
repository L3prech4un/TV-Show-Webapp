"""creates.py: contains association tables for many to many relationships"""
from db.server import db

# join table between user and post
Creates = db.Table(
  'Creates',
  # grab the UserID primary key and make it a foreign key
  db.Column('UserID', db.Integer, db.ForeignKey('User.UserID')),
  # grab the PostID primary key and make it a foreign key
  db.Column('PostID', db.Integer, db.ForeignKey('Post.PostID'))
)