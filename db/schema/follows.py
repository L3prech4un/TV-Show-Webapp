"""follows.py: contains association tables for many to many relationships"""
from db.server import db

# join table between user and comment
Follows = db.Table(
  'Follows',
  # grab the UserID primary key and make it a foreign key
  db.Column('UserID', db.Integer, db.ForeignKey('User.UserID')),
  # grab the UserID primary key and make it a foreign key
  db.Column('FollowerID', db.Integer, db.ForeignKey('User.UserID'))
)