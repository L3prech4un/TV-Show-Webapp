"""makes.py: contains association tables for many to many relationships"""
from sqlalchemy import Table, Column, Integer, ForeignKey
from db.server import Base
# join table between user and comment
Makes = Table(
  'makes',
  Base.metadata,
  # grab the UserID primary key and make it a foreign key
  Column('UserID', Integer, ForeignKey('user.UserID')),
  # grab the CommentID primary key and make it a foreign key
  Column('CommentID', Integer, ForeignKey('comment.CommentID'))
)