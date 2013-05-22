from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from cmsflask.auth import requires_auth
from cmsflask.models import Post, Content, Category, Comment

admin = Blueprint('admin', __name__, template_folder='templates')

def register_api(app, view_class, endpoint, url, pk='id', pk_type='int'):
    view_func = view_class.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET'])
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])

def register_crud(app, view_class, endpoint, url, pk='id', pk_type='int'):
    app.add_url_rule('%s%s' % (url, endpoint) , view_func=view_class.as_view('index'))
    app.add_url_rule('%s%s/%s' % (url, endpoint, 'create'), defaults={pk: None}, view_func=view_class.as_view('create'))
    app.add_url_rule('%s%s/%s/<%s:%s>' % (url, endpoint, 'edit', pk_type, pk), view_func=view_class.as_view('edit'))
    app.add_url_rule('%s%s/%s/<%s:%s>' % (url, endpoint, 'delete', pk_type, pk), view_func=view_class.as_view('delete'))

class AdminContent(MethodView):
    cls = Content
    decorators = [requires_auth]
    # Map post types to models
    class_map = {
        'post': Post,
        'category': Category,
        'comment': Comment,
    }


    def _get_context(self, slug=None):

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
        if slug:
            context = self._get_context(slug)
            return render_template('admin/detail.html', **context)
        else:
            cs= self.cls.objects.all()
            return render_template('admin/list.html', contents=cs)

    def post(self):
        #create a content
        context = self.get_context()
        form = context.get('form')

        if form.validate():
            content = context.get('content')
            form.populate_obj(content)
            content.save()

            return redirect(url_for('admin.content'))
        return render_template('admin/detail.html', **context)

    def delete(self, slug):
        content = self._get_context(slug)
        content.delete()
        return redirect(url_for('admin.content'))

    def put(self, slug):
        #update a single content
        return self.post(self,slug)

"""
    decorators = [requires_auth]
    # Map post types to models
    class_map = {
        'post': Post,
        'category': Category,
        'comment': Comment,
    }

    cls = Content



    def get(self, slug):
        if slug:
            context = self.get_context(slug)
            return render_template('admin/detail.html', **context)
        else:
            cs= self.cls.objects.all()
            return render_template('admin/list.html', contents=cs)

    def post(self, slug):
        #create a content
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            content = context.get('content')
            form.populate_obj(content)
            content.save()

            return redirect(url_for('admin.index'))
        return render_template('admin/detail.html', **context)

    def put(self, slug):
        #update a single content
        self.post(self,slug)
"""
# Register the urls
#admin.add_url_rule('/admin/', view_func=List.as_view('index'))
#admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
#admin.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))
#admin.add_url_rule('/admin/delete/<slug>/', view_func=Detail.as_view('delete'))
#app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])

register_api(admin, AdminContent, 'content', '/admin/', pk='slug', pk_type='string')
register_crud(admin, AdminContent, 'content', '/admin/', pk='slug', pk_type='string')