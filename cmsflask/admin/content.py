from flask import Blueprint,render_template
from cmsflask.models import Post, Content, Category, Comment

class_map = {
        'post': Post,
        'category': Category,
        'comment': Comment,
        'content': Content,
    }

base_url = '/admin/'

admin_content = Blueprint('admin_content', __name__, template_folder='templates')

@admin_content.route(base_url, methods=['GET'])
def index():
    cs= Content.objects.all()
    return render_template('admin/content/list.html', contents=cs)
