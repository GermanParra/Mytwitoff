from flask_sqlalchemy import SQLAlchemy

# Create a DB Object
# opening up the db connection
DB = SQLAlchemy()


# Make a User Table by creating a User Class

class User(DB.Model):
    '''Creates a User Table with SQLAlchemy'''
    # id column schema
    id = DB.Column(DB.BigInteger, primary_key = True, nullable = False)
    # username column schema
    username = DB.Column(DB.String, nullable = False)

# Make a Tweet Table by creating a tweet Class

class Tweet(DB.Model):
    '''Creates a Tweet Table with SQLAlchemy'''
    # id column schema
    id = DB.Column(DB.BigInteger, primary_key = True, nullable=False)
    # text column schema
    text = DB.Column(DB.Unicode(300), nullable=False) # Unicode allows for both text and links and emojis, etc.

    # User Column schema
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)

    # Set up a relationship between tweets and IDs
    # This will automatically add a new id to both the tweet and the user
    # making sure it goes both ways
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))