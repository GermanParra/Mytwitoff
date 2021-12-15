from os import getenv
from flask import Flask, render_template, request
from twitoff.twitter import add_or_update_user
from .models import DB, User, Tweet
from .twitter import add_or_update_user, get_all_usernames
from .predict import predict_user


# Create a 'factory' for serving up the app when is launched
def create_app():
    # initializes our app
    app = Flask(__name__)

    # Database configurations
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Turn off verification when we request changes to db
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URI')

    # Give our APP access to our database
    DB.init_app(app)

    # Listen to a "route"
    # Make our "Home" "root" route. '/' is the home page route
    @app.route('/')
    def root():
        # what i want to happen when somebody goes to the home page
        # Query users to display on the home page
        return render_template('base.html', title = "Home", users = User.query.all())

    @app.route('/update')
    def update():
        '''update all users'''
        usernames = get_all_usernames()
        for username in usernames:
            add_or_update_user(username)
        return render_template('base.html',title="All users have been updated to include their latest tweets")

    @app.route('/reset')
    def reset():
        # remove everything from database
        DB.drop_all()
        # Create the database file initially
        DB.create_all()
        return render_template('base.html', title = 'Database Reset')


    # API ENDPOINTS (Quering and manipulating data in a database)
    # this routes are NOT just displaying information

    # this route is going to change our Database
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        # request.values is pulling data from the html
        # use the username from the URL (route)
        # or grab it from the dropdown
        name = name or request.values['user_name']

        # If the user exist in the db already, update it, and query for it

        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f"User '{name}' Successfully Added!"
            # From the user that was just added / Updated
            # get their tweets to display on the /user/<name> page
            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = f"Error adding {name}: {e}"

            tweets = []

        return render_template('user.html', title=name, tweets=tweets, message=message)


    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = 'Cannot compare a user to themselves!'
        else:
            tweet_text = request.values['tweet_text']
            prediction = predict_user(user0, user1, tweet_text)
            if prediction == 0:
                predicted_user = user0
                non_predicted_user = user1
            else:
                predicted_user = user1
                non_predicted_user = user0

            message = f'"{tweet_text}" is more likely to be said by {predicted_user} than {non_predicted_user}'

        return render_template('prediction.html', title='Prediction', message=message)




    return app



    
    # # kind of like what jinja2 does to our web pages
    # app_title = 'Mytwitoff DS33'

    # @app.route('/test')
    # def test():
    #     return f"A page from {app_title} app"

    # @app.route('/hola')
    # def hola():
    #     return "Hola, Twitoff!"

    # @app.route('/salut')
    # def salute():
    #     return "Salute, Twitoff!"