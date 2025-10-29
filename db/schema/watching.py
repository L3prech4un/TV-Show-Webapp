"""watching.py: contains association tables for many to many relationships"""
from sqlalchemy import Table, Column, Integer, ForeignKey
from db.server import Base

# join table between user and comment
Watching = Table(
  'Watching',
  Base.metadata,
  # grab the UserID primary key and make it a foreign key
  Column('UserID', Integer, ForeignKey('User.UserID')),
  # grab the MediaID primary key and make it a foreign key
  Column('MediaID', Integer, ForeignKey('TVMovie.MediaID')))