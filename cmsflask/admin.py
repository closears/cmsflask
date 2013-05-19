from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from cmsflask.auth import requires_auth
from cmsflask.models import Post, Content, Category, Comment

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
    decorators = [requires_auth]
    cls = Content

    def get(self):
        posts = self.cls.objects.all()
        return render_template('admin/list.html', posts=posts)


class Detail(MethodView):

    decorators = [requires_auth]
    # Map post types to models
    class_map = {
        'post': Post,
        'category': Category,
        'comment': Comment,
    }

    def get_context(self, slug=None):

        if slug:
            content = Content.objects.get_or_404(slug=slug)
            # Handle old posts types as well
            cls = content.__class__ if content.__class__ != Content else Post
            form_cls = model_form(cls,  exclude=('created_at', 'modified_at', 'comments', 'slug'))
            if request.method == 'POST':
                form = form_cls(request.form, inital=content._data)
            else:
                form = form_cls(obj=content)
        else:
            # Determine which post type we need
            cls = self.class_map.get(request.args.get('type', 'content'))
            content = cls()
            if isinstance(content, Post):
                form_cls = model_form(cls,  exclude=('created_at', 'modified_at', 'comments', 'slug'))
            elif isinstance(content, Category):
                form_cls = model_form(cls,  exclude=('created_at', 'modified_at', 'slug', 'contents'))
            elif isinstance(content, Comment):
                form_cls = model_form(cls,  exclude=('created_at', 'modified_at'))

            form = form_cls(request.form)
        context = {
            "content": content,
            "form": form,
            "create": slug is None
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('admin/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            content = context.get('content')
            form.populate_obj(content)
            content.save()

            return redirect(url_for('admin.index'))
        return render_template('admin/detail.html', **context)


# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))
admin.add_url_rule('/admin/delete/<slug>/', view_func=Detail.as_view('delete'))
