"""users.py: create a table named 'Users' using SQLAlchemy"""
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from db.server import Base

# Association table for many-to-many relationship between Users and Followers
followers = Table(
    'Followers',
    Base.metadata,
    Column("FollowerID", Integer, ForeignKey("User.UserID"), primary_key=True),
    Column("FollowedID", Integer, ForeignKey("User.UserID"), primary_key=True)
)

class Users(Base):
    __tablename__ = 'User'

    UserID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    FirstName = Column(String(40), nullable=False)
    LastName = Column(String(40), nullable=False)
    Username = Column(String(20), unique=True, nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    Password = Column(String(256), nullable=False)

    # Users that this user is following:
    following = relationship(
        "Users",
        secondary=followers,
        primaryjoin=UserID == followers.c.FollowerID,
        secondaryjoin=UserID == followers.c.FollowedID,
        backref="followers"
    )

    def __repr__(self):
        return f"""
            "FIRST NAME: {self.FirstName},
             LAST NAME: {self.LastName},
             USERNAME: {self.Username},
             EMAIL: {self.Email},
             PASSWORD: {self.Password}
        """