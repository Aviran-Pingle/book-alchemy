import os

from flask import Flask

from datamanager import db
from routes import bp


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config.update(
        {
            'SQLALCHEMY_DATABASE_URI':
                f'sqlite:///{os.path.join(basedir, "data/library.sqlite")}',
            'SECRET_KEY': os.urandom(24)
        }
    )
    db.init_app(app)
    app.register_blueprint(bp)
    return app


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)


if __name__ == '__main__':
    main()
