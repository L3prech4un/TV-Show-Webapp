"""post.py: create a table named post in the TV-SHOW-WEBAPP database"""
from db.server import db

class Post(db.Model):
    __tablename__ = 'Post'
    # db.<data type> is the data type of the value in the column
    PostID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    MediaID = db.Column(db.Integer,db.ForeignKey('TVMovie.MediaID'))
    # 40 = max length of string
    Title = db.Column(db.String(40))
    Date = db.Column(db.String(40))
    Content = db.Column(db.String(40))

    # create relationship with user table. assoc table name = Creates
    User = db.relationship('User', secondary = 'Creates', back_populates = 'Post')
    # create relationship with comment table
    Comment = db.relationship('Comment', back_populates = 'Post')
    # create relationship with TVMovie table
    TVMovie = db.relationship('TVMovie', back_populates = 'Post')

    def __init__(self, name):
        self.Title = self.Title
        self.Date= self.Date
        self.Content = self.Content

    def __repr__(self):
        return f"""
            "TITLE: {self.Title},
             DATE: {self.Date},
             CONTENT: {self.Content}
        """
    
    def __repr__(self):
        return self.__repr__()
