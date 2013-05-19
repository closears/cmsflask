import datetime
from flask import url_for
from cmsflask import db
from slugify import slugify

class Content(db.DynamicDocument):
    description = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    modified_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    def __unicode__(self):
        return self.description[0:64]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        return super(Content, self).save(*args, **kwargs)

    @property
    def type(self):
        return self.__class__.__name__.lower()

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', '-modified_at'],
        'ordering': ['-modified_at']
    }

class SlugW(Content):
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True, unique=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        return super(SlugW, self).save(*args, **kwargs)

    meta = {
        'allow_inheritance': True,
        'indexes': ['slug'],
    }

class Post(SlugW):
    order = db.IntField(min_value=0)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    categories = db.ListField(db.ReferenceField('Category',dbref=True))


class Comment(Content):
    author = db.StringField(max_length=255, required=True)

class Category(SlugW):
    img = db.StringField(max_length=512)
