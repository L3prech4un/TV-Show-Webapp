"""tvmovie.py: create a table named tvmovie in the TV-SHOW-WEBAPP database"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.server import Base

class TVMovie(Base):
    __tablename__ = 'TVMovie'
    MediaID = Column(Integer,primary_key=True)
    # 40 = max length of string
    Title = Column(String(40))
    Genre = Column(String(40))
    Year = Column(String(40))
    Type = Column(String(40))

    # create relationship with user table. assoc table name = Watching
    watchingUser = relationship('User', secondary = 'Watching', back_populates = 'TVMovieWatching')
    # create relationship with user table. assoc table name = Watched
    watchedUser = relationship('User', secondary = 'Watched', back_populates = 'TVMovieWatched')
    # create relationship with user table. assoc table name = Watchlist
    watchlistUser = relationship('User', secondary = 'Watchlist', back_populates = 'TVMovieWatchlist')
    # create relationship with post table
    Post = relationship('Post', back_populates = 'TVMovie')


    def __repr__(self):
        return f"""
            "TITLE: {self.Title},
             GENRE: {self.Genre},
             YEAR: {self.Year},
             TYPE: {self.Type}
        """
    
    def __repr__(self):
        return self.__repr__()
