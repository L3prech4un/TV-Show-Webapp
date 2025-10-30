"""user.py: create a table named user in the TV-SHOW-WEBAPP database"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.server import Base
from db.schema.creates import Creates
from db.schema.makes import Makes
from db.schema.watched import Watched
from db.schema.watching import Watching
from db.schema.watchlist import Watchlist
from db.schema.follows import Follows

class User(Base):
    __tablename__ = 'user'
    UserID = Column(Integer,primary_key=True,autoincrement=True)
    # 40 = max length of string
    FName = Column(String(40))
    LName = Column(String(40))
    UName = Column(String(40))
    PWord = Column(String(40))
    Email = Column(String(40))

    # create relationship with post table. assoc table name = Creates
    Post = relationship('Post', secondary = Creates, back_populates = 'User')
    # create relationship with comment table. assoc table name = Makes
    Comment = relationship('Comment', secondary = Makes, back_populates = 'User')
    # create relationship with TVMovie table. assoc table name = watched
    TVMovieWatched = relationship('TVMovie', secondary = Watched, back_populates = 'watchedUser')
    # create relationship with TVMovie table. assoc table name = watching
    TVMovieWatching= relationship('TVMovie', secondary = Watching, back_populates = 'watchingUser')
    # create relationship with TVMovie table. assoc table name = watchlist
    TVMovieWatchlist = relationship('TVMovie', secondary = Watchlist, back_populates = 'watchlistUser')
    # self-referential many-to-many for follows (followers / following)
    # defined after class so User is available for join expressions

    def __repr__(self):
        return f"""
            "FIRST NAME: {self.FName},
             LAST NAME: {self.LName},
             USER NAME: {self.UName},
             PASSWORD: {self.PWord},
             EMAIL: {self.Email}
        """
    
    def __repr__(self):
        return self.__repr__()

# define self-referential followers / following relationship after class definition
User.followers = relationship(
    'User',
    secondary=Follows,
    primaryjoin=(User.UserID == Follows.c.UserID),
    secondaryjoin=(User.UserID == Follows.c.FollowerID),
    foreign_keys=[Follows.c.UserID, Follows.c.FollowerID],
    backref='following'
)
