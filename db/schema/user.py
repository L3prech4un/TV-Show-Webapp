"""user.py: create a table named user in the TV-SHOW-WEBAPP database"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.server import Base

class User(Base):
    __tablename__ = 'User'
    UserID = Column(Integer,primary_key=True,autoincrement=True)
    # 40 = max length of string
    FName = Column(String(40))
    LName = Column(String(40))
    UName = Column(String(40))
    PWord = Column(String(40))
    Email = Column(String(40))
    DOB = Column(String(40))

    # create relationship with post table. assoc table name = Creates
    Post = relationship('Post', secondary = 'Creates', back_populates = 'User')
    # create relationship with comment table. assoc table name = Makes
    Post = relationship('Comment', secondary = 'Makes', back_populates = 'User')
    # create relationship with TVMovie table. assoc table name = watched
    Post = relationship('TVMovie', secondary = 'Watched', back_populates = 'User')
    # create relationship with TVMovie table. assoc table name = watching
    Post = relationship('TVMovie', secondary = 'Watching', back_populates = 'User')
    # create relationship with TVMovie table. assoc table name = watchlist
    Post = relationship('TVMovie', secondary = 'Watchlist', back_populates = 'User')
    # create relationship with User table. assoc table name = follows
    Post = relationship('User', secondary = 'Follows', back_populates = 'User')

    def __init__(self, name):
        self.FName = self.FName
        self.LName = self.LName
        self.UName = self.UName
        self.PWord = self.PWord
        self.Email = self.Email
        self.DOB = self.DOB

    def __repr__(self):
        return f"""
            "FIRST NAME: {self.FName},
             LAST NAME: {self.LName},
             USER NAME: {self.UName},
             PASSWORD: {self.PWord},
             EMAIL: {self.Email},
             DATE OF BIRTH: {self.DOB}
        """
    
    def __repr__(self):
        return self.__repr__()
