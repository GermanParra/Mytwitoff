from flask import Flask, render_template
from .models import DB, User, Tweet

def create_app():
    # initializes our app
    app = Flask(__name__)

    # Database configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Give our APP access to our database
    DB.init_app(app)

    # Listen to a "route"
    # '/' is the home page route
    @app.route('/')
    def root():
        # query the DB for all users
        users = User.query.all()
        #what i want to happen when somebody goes to the home page

        return render_template('base.html', title = "Home", users = users)

    @app.route('/populate')
    def populate():
        ger = User(id=1, username='Ger')
        DB.session.add(ger)
        scarlet = User(id=2, username='Yuruani')
        DB.session.add(scarlet)
        tweet1 = Tweet(id=1, text='Ger tweet text', user=ger)
        DB.session.add(tweet1)
        tweet2 = Tweet(id=2, text='Yuruani tweet text', user=scarlet)
        DB.session.add(tweet2)
        #save database
        DB.session.commit()
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