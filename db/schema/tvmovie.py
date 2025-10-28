"""tvmovie.py: create a table named tvmovie in the TV-SHOW-WEBAPP database"""
from db.server import db

class TVMovie(db.Model):
    __tablename__ = 'TVMovie'
    # db.<data type> is the data type of the value in the column
    MediaID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # 40 = max length of string
    Title = db.Column(db.String(40))
    Genre = db.Column(db.String(40))
    Year = db.Column(db.String(40))
    Type = db.Column(db.String(40))

    # create relationship with user table. assoc table name = Watching
    User = db.relationship('User', secondary = 'Watching', back_populates = 'TVMovie')
    # create relationship with user table. assoc table name = Watched
    User = db.relationship('User', secondary = 'Watched', back_populates = 'TVMovie')
    # create relationship with user table. assoc table name = Watchlist
    User = db.relationship('User', secondary = 'Watchlist', back_populates = 'TVMovie')
    # create relationship with post table
    Post = db.relationship('Post', back_populates = 'TVMovie')

    def __init__(self, name):
        self.Title = self.Title
        self.Genre = self.Genre
        self.Year = self.Year
        self.Type = self.Type

    def __repr__(self):
        return f"""
            "TITLE: {self.Title},
             GENRE: {self.Genre},
             YEAR: {self.Year},
             TYPE: {self.Type}
        """
    
    def __repr__(self):
        return self.__repr__()
