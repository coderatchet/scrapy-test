from mongoengine import Document, StringField, DateTimeField

class Article(Document):
    """ Document Object for storing news article data. """
    meta = {'db_alias': 'default'}

    title = StringField(required=True)
    content = StringField(required=True)
    date_time = DateTimeField()
    author = StringField()
