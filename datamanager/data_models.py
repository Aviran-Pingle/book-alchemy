from datamanager import db


class Author(db.Model):
    """
    Represents an Author in the database.

    Attributes:
        id (int): Primary key, auto-incrementing ID for the author.
        name (str): Name of the author.
        birth_date: Date of birth of the author.
        date_of_death: Date of death of the author (if applicable).
    """

    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return (f"Author(id={self.id},"
                f" name='{self.name}',"
                f" birth_date='{self.birth_date}',"
                f" date_of_death='{self.date_of_death}')")

    def __str__(self):
        birth_date_str = self.birth_date.strftime(
            '%Y-%m-%d') if self.birth_date else "Unknown"
        date_of_death_str = self.date_of_death.strftime(
            '%Y-%m-%d') if self.date_of_death else "Unknown"
        return (f"Author: {self.name}\n"
                f"ID: {self.id}\n"
                f"Birth Date: {birth_date_str}\n"
                f"Date of Death: {date_of_death_str}")


class Book(db.Model):
    """
    Represents a Book in the database.

    Attributes:
        id (int): Primary key, auto-incrementing ID for the book.
        isbn (str): ISBN (International Standard Book Number) of the book.
        title (str): Title of the book.
        publication_year (int): Year of publication of the book.
        author_id (int): Foreign key referencing the ID of the corresponding
        author.
    """

    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    cover_image_url = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'),
                          nullable=False)

    def __repr__(self):
        return (f"Book(id={self.id},"
                f" isbn='{self.isbn}',"
                f" title='{self.title}',"
                f" publication_year={self.publication_year},"
                f" author_id={self.author_id})")

    def __str__(self):
        return (f"Book Title: {self.title}\n"
                f"ISBN: {self.isbn}\n"
                f"Publication Year: {self.publication_year}\n"
                f"Author: {self.author.name}\n"
                f"Author ID: {self.author_id}")
