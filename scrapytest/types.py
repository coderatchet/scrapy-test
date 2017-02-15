from mongoengine import Document, StringField


class Article(Document):
    """ Document Object for storing news article data. """
    title = StringField(required=True)
    content = StringField(required=True)
    author = StringField(required=False)