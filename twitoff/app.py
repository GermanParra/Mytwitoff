from flask import Flask, render_template
from twitoff.twitter import add_or_update_user
from .models import DB, User, Tweet
from .twitter import add_or_update_user, get_all_usernames

# Create a 'factory' for serving up the app when is launched
def create_app():
    # initializes our app
    app = Flask(__name__)

    # Database configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Turn off verification when we request changes to db

    # Give our APP access to our database
    DB.init_app(app)

    # Listen to a "route"
    # Make our "Home" "root" route. '/' is the home page route
    @app.route('/')
    def root():
        # query the DB for all users
        users = User.query.all()
        #what i want to happen when somebody goes to the home page
        return render_template('base.html', title = "Home", users = users)

    @app.route('/update')
    def update():
        '''update all users'''
        usernames = get_all_usernames()
        for username in usernames:
            add_or_update_user(username)
        return "Updated"

    @app.route('/populate')
    def populate():
        add_or_update_user('NASA')
        add_or_update_user('elonmusk')
        return '''Created some users.
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset </a>
        <a href='/populate'>Go to Populate </a>'''

    @app.route('/reset')
    def reset():
        # remove everything from database
        DB.drop_all()
        # Create the database file initially
        DB.create_all()
        return '''The database has been reset.
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>'''

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