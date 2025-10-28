"""watching.py: contains association tables for many to many relationships"""
from db.server import db

# join table between user and comment
Watching = db.Table(
  'Watching',
  # grab the UserID primary key and make it a foreign key
  db.Column('UserID', db.Integer, db.ForeignKey('User.UserID')),
  # grab the MediaID primary key and make it a foreign key
  db.Column('MediaID', db.Integer, db.ForeignKey('TVMovie.MediaID')))