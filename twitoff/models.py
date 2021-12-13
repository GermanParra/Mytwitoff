from flask_sqlalchemy import SQLAlchemy

# Create a DB Object
DB = SQLAlchemy()


# Make a User Table by creating a User Class

class User(DB.Model):
    '''Creates a User Table with SQLAlchemy'''
    # id column
    id = DB.Column(DB.BigInteger, primary_key = True)
    # username column
    username = DB.Column(DB.String, nullable = False)

# Make a Tweet Table by creating a tweet Class

class Tweet(DB.Model):
    '''Creates a Tweet Table with SQLAlchemy'''
    # id column
    id = DB.Column(DB.BigInteger, primary_key = True)
    # text column
    text = DB.Column(DB.Unicode(300)) # Unicode allows for both text and links and emojis, etc.

    # Create a relationship between a tweet and a user
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)

    # Finalizing the relationship making sure it goes both ways
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))