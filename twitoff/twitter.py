'''Handles connection to Twitter API using Tweepy'''

from os import getenv # Gets enviroment variables (.env)
import tweepy # Help to get right information from Twitter API
import spacy # word embeddings tools
from .models import DB, Tweet, User


# Get API keys from .env
KEY = getenv('TWITTER_API_KEY')
SECRET = getenv('TWITTER_API_KEY_SECRET')

# Connect to the Twitter API
TWITTER_AUTH = tweepy.OAuthHandler(KEY, SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

# Load our pretrained SpaCy Word Embeddings model
nlp = spacy.load('my_model/')

# Turn tweet text into word embeddings
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

# fuction to query the API for a user
# and add the user to the DB

def add_or_update_user(username):
    """
    Gets twitter user and tweets from DB
    Gets user by "username" parameter.
    """
    try:
        # get a twitter user from the API
        twitter_user = TWITTER.get_user(screen_name=username)

        # Check to see if that user already exist in our database
        # If the user is already in the database, cool, grab that user
        # If the user is not already in the database, make a new user in the database.
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, username=username)

        # add the user to the DB if they don't already exists.
        DB.session.add(db_user)

        # Grab the recent 200 tweets of our twitter_user and drop all retweets and replies
        tweets = twitter_user.timeline(
            count=200,
            exclude_replies =True,
            include_rts=False,
            tweet_mode="extended",
            since_id=db_user.newest_tweet_id)

        # Check to see if the newest tweet in DB is equal to the newest tweet from Twitter API
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # add the individual tweets to the DB session (tweets is a list of tweet objects)
        for tweet in tweets:
            # type(tweet) == object
            # Turn each tweet into word embedding. (vectorization)
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(
                id=tweet.id,
                text=tweet.full_text[:300],
                vect=tweet_vector
                )

            # make sure the tweet is connected to our user
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"ERROR processing {username}: {e}")
        # Make sure my whole application kwnows about this error
        raise e

    else:
        # Commit "save" the changes to the DB
        DB.session.commit()

def get_all_usernames():
    '''Gets the usernames of all users that are already in the Database'''
    usernames = []
    Users = User.query.all()
    for user in Users:
        usernames.append(user.username)

    return usernames