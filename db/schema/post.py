"""post.py: create a table named post in the TV-SHOW-WEBAPP database"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.server import Base
from db.schema.creates import Creates


class Post(Base):
    __tablename__ = 'post'
    PostID = Column(Integer,primary_key=True,autoincrement=True)
    MediaID = Column(Integer,ForeignKey('tvmovie.MediaID'))
    # 40 = max length of string
    Title = Column(String(40))
    Date = Column(String(40))
    Content = Column(String(250))
    Spoiler = Column(Boolean)
    Rating = Column(Integer)

    # create relationship with user table. assoc table name = Creates
    User = relationship('User', secondary = Creates, back_populates = 'Post')
    # create relationship with comment table
    Comment = relationship('Comment', back_populates = 'Post')
    # create relationship with TVMovie table
    TVMovie = relationship('TVMovie', back_populates = 'Post')

    def __repr__(self):
        return f"""
            "TITLE: {self.Title},
             DATE: {self.Date},
             CONTENT: {self.Content}
        """
    
    def __repr__(self):
        return self.__repr__()
