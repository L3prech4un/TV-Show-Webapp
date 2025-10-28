"""makes.py: contains association tables for many to many relationships"""
from db.server import db

# join table between user and comment
Makes = db.Table(
  'Makes',
  # grab the UserID primary key and make it a foreign key
  db.Column('UserID', db.Integer, db.ForeignKey('User.UserID')),
  # grab the CommentID primary key and make it a foreign key
  db.Column('CommentID', db.Integer, db.ForeignKey('Comment.CommentID'))
)