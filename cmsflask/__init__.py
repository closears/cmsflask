from flask import Flask
from flask.ext.mongoengine import MongoEngine
from cmsflask import mongocfg

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = mongocfg.MONGODB_SETTINGS
app.config["SECRET_KEY"] = "supersecretkey"

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()

def register_blueprints(app):
    from cmsflask.views import posts
    from cmsflask.admin import admin
    app.register_blueprint(posts)
    app.register_blueprint(admin)

register_blueprints(app)
