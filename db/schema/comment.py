"""comment.py: create a table named comment in the TV-SHOW-WEBAPP database"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.server import Base

class Comment(Base):
    __tablename__ = 'Comment'
    CommentID = Column(Integer,primary_key=True,autoincrement=True)
    PostID = Column(Integer,ForeignKey('Post.PostID'))
    # 40 = max length of string
    Date = Column(String(40))
    Content = Column(String(40))

    # create relationship with user table. assoc table name = makes
    User = relationship('User', secondary = 'Makes', back_populates = 'Comment')
    # create relationship with post table
    Post = relationship('Post', back_populates = 'Comment')

    def __init__(self, name):
        self.Date = self.Date
        self.Content = self.Content

    def __repr__(self):
        return f"""
            "DATE: {self.Date},
             CONTENT: {self.Content}
        """
    
    def __repr__(self):
        return self.__repr__()
