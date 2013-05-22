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
    from cmsflask.admin.content import admin_content
    from cmsflask.errors import errors
    app.register_blueprint(posts)
    app.register_blueprint(admin_content)
    app.register_blueprint(errors)

register_blueprints(app)
