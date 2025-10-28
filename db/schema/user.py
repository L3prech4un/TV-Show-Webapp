"""user.py: create a table named user in the TV-SHOW-WEBAPP database"""
from db.server import db

class User(db.Model):
    __tablename__ = 'User'
    # db.<data type> is the data type of the value in the column
    UserID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # 40 = max length of string
    FName = db.Column(db.String(40))
    LName = db.Column(db.String(40))
    UName = db.Column(db.String(40))
    PWord = db.Column(db.String(40))
    Email = db.Column(db.String(40))
    DOB = db.Column(db.String(40))

    # create relationship with post table. assoc table name = Creates
    Post = db.relationship('Post', secondary = 'Creates', back_populates = 'User')
    # create relationship with comment table. assoc table name = Makes
    Post = db.relationship('Comment', secondary = 'Makes', back_populates = 'User')
    # create relationship with TVMovie table. assoc table name = watched
    Post = db.relationship('TVMovie', secondary = 'Watched', back_populates = 'User')
    # create relationship with TVMovie table. assoc table name = watching
    Post = db.relationship('TVMovie', secondary = 'Watching', back_populates = 'User')
    # create relationship with TVMovie table. assoc table name = watchlist
    Post = db.relationship('TVMovie', secondary = 'Watchlist', back_populates = 'User')
    # create relationship with User table. assoc table name = follows
    Post = db.relationship('User', secondary = 'Follows', back_populates = 'User')

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
