from flask import Flask
import os
# from .extensions import mongo, cors

from app.webhook.routes import webhook
from flask import Flask
from .extensions import mongo, cors

# Creating our flask app
def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, '..', 'templates')

    # Pass the correct string path
    app = Flask(__name__, template_folder=template_dir)
    app.config["MONGO_URI"] = "mongodb+srv://Muskan:muskan198@cluster0.rqhyigo.mongodb.net/github"
    mongo.init_app(app)
    cors.init_app(app)

    
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
