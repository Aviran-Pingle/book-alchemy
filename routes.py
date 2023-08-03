from flask import Blueprint, request, render_template, flash, redirect, url_for

import datamanager.operations as ops

bp = Blueprint('routes', __name__, template_folder='templates')


@bp.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Handle the addition of a new author.

    If the HTTP method is POST, this function receives form data,
    and adds a new author to the database.
    If the author's birthdate is after the date of death (if provided),
    the addition is considered invalid.

    Returns:
        A rendered HTML template for adding a new author.
    """
    if request.method == 'POST':
        if not ops.add_author(request.form):
            flash('Invalid Dates', 'danger')
        else:
            flash('Author Added Successfully', 'success')

    return render_template('add_author.html')


@bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handle the addition of a new book.

    If the HTTP method is POST, this function receives form data, creates a
    new book record in the database,and associates it with an existing
    author.
    Display a flash message for successful book addition.

    Returns: A rendered HTML template for adding a new book with a list of
    available authors.
    """
    if request.method == 'POST':
        ops.add_book(request.form)
        flash('Book Added Successfully', 'success')
    return render_template('add_book.html', authors=ops.get_authors())


@bp.route('/', methods=['GET', 'POST'])
def homepage():
    """
    Display the homepage with a list of books.
    Fetches books from the database based on filter and sort options.

    Returns:
        A rendered HTML template for the homepage with a list of books.
    """
    term = request.form.get('filter')
    sort = request.form.get('sort')
    books = books=ops.get_books(sort, term)
    if term and not books:
        flash('No matching books', 'warning')
    return render_template('home.html', books=books)


@bp.route('/book/<int:book_id>')
def delete_book(book_id):
    """
    Delete a book from the database.

    Parameters:
        book_id (int): The unique identifier of the book to be deleted.

    Returns:
        A redirect to the homepage after deleting the book,
        with a flash message indicating success.

    """
    ops.delete_book(book_id)
    flash('Book Deleted Successfully', 'success')
    return redirect(url_for('routes.homepage'))
