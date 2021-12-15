from .models import User
import numpy as np
from sklearn.linear_model import LogisticRegression
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    '''Take in two usernames,
    query for the tweet vectorizations for those 2 users,
    compile the vectorizations into an X matrix
    generate a numpy array of labels (y variable)
    vectorize the hypotetical tweet text
    generate and return a prediction'''

    # Query for our 2 users
    user0 = User.query.filter(User.username == user0_name).one()
    user1 = User.query.filter(User.username == user1_name).one()

    # Get the Tweet vectorizations for the 2 users
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])
    # Combine the vectors into an X Matrix
    X = np.vstack([user0_vects, user1_vects])

    # Generate labels and 0s and 1s for a y vector
    zeros = np.zeros(len(user0.tweets))
    ones = np.ones(len(user1.tweets))
    y = np.concatenate([zeros, ones])

    # fit our LogisticRegression model
    log_reg = LogisticRegression().fit(X,y)

    # vectorize our hypotetical tweet text
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # return the predicted label: (0 or 1)
    # reshaping to make a 2D Numpy array from a 1D Numpy array by using extra brackets
    prediction = log_reg.predict([hypo_tweet_vect])
    
    return  prediction[0]