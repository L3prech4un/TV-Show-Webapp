"""comment.py: create a table named comment in the TV-SHOW-WEBAPP database"""
from db.server import db

class Comment(db.Model):
    __tablename__ = 'Comment'
    # db.<data type> is the data type of the value in the column
    CommentID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    PostID = db.Column(db.Integer,db.ForeignKey('Post.PostID'))
    # 40 = max length of string
    Date = db.Column(db.String(40))
    Content = db.Column(db.String(40))

    # create relationship with user table. assoc table name = makes
    User = db.relationship('User', secondary = 'Makes', back_populates = 'Comment')
    # create relationship with post table
    Post = db.relationship('Post', back_populates = 'Comment')

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
