from datetime import datetime

from sqlalchemy import or_

from datamanager import db
from datamanager.data_models import Author, Book


def add_author(form_data: dict):
    """
    Add a new author to the database.

    Parameters:
        form_data (dict): The form data containing the author's name,
        birthdate, and date of death.

    Returns:
        bool: True if the author was added successfully, False otherwise.
        """
    name = form_data['name']
    birthdate = (datetime.strptime(form_data['birthdate'], '%Y-%m-%d')
                 .date())
    date_of_death = form_data['date_of_death']
    date_of_death = (datetime.strptime(date_of_death, '%Y-%m-%d')
                     .date() if date_of_death else None)

    if date_of_death and date_of_death < birthdate:
        return False

    new_author = Author(name=name, birth_date=birthdate,
                        date_of_death=date_of_death)
    db.session.add(new_author)
    db.session.commit()
    return True


def add_book(form_data: dict):
    """
    Add a new book to the database.

    Parameters:
        form_data (dict): The form data containing the book's ISBN, title,
        publication year, and author ID.
    """
    isbn = form_data['isbn']
    title = form_data['title']
    publication_year = form_data['publication_year']
    author_id = form_data['author']
    cover_image = f'https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg'

    new_book = Book(isbn=isbn, title=title, publication_year=publication_year,
                    cover_image_url=cover_image, author_id=author_id)
    db.session.add(new_book)
    db.session.commit()


def get_authors():
    """
    Retrieve a list of all authors from the database.
    """
    return Author.query.all()


def get_books(sort_by: str, search_term: str):
    """
    Retrieve a list of books based on sorting and filtering options.

    Parameters:
        sort_by (str): The sorting option. Possible values: 'title', 'author'.
        search_term (str): The search term to filter books by title or
        author name.

    Returns:
        List[Book]: A list of Book objects that match the options.
    """
    if search_term:
        return Book.query.join(Author).filter(
            or_(Book.title.ilike(f'%{search_term}%'),
                Author.name.ilike(f'%{search_term}%'))
        ).all()

    if sort_by == 'title':
        return Book.query.order_by(Book.title).all()

    if sort_by == 'author':
        return Book.query.join(Author).order_by(Author.name).all()

    return Book.query.all()


def check_author_books(author_id: int):
    """
    Check if an author has any associated books.
    If not, delete the author from the database.

    Parameters:
        author_id (int): The unique identifier of the author.
    """
    author = db.get_or_404(Author, author_id)
    if not author.books:
        db.session.delete(author)
        db.session.commit()


def delete_book(book_id: int):
    """
    Delete a book from the database.

    Parameters:
        book_id (int): The unique identifier of the book to be deleted.
    """
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    check_author_books(book.author_id)
