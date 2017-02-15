class Article:
    """ Object for storing news article data. """

    def __init__(self, id, title, content, author=None):
        super().__init__()
        self._id = id
        self._title = title
        self._content = content
        self._author = author
