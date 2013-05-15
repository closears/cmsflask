from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "cms_flask_db"}
app.config["SECRET_KEY"] = "asdfasdfasdfasdfasdf"

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()

def register_blueprints(app):
    # Prevents circular imports
    from cmsflask.views import posts
    from cmsflask.admin import admin
    app.register_blueprint(posts)
    app.register_blueprint(admin)

register_blueprints(app)
