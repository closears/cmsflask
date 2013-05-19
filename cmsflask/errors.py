from flask import render_template, Blueprint
from cmsflask import app

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=e, error_num=404), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', error=e, error_num=500), 500

errors = Blueprint('errors', __name__, template_folder='templates')
