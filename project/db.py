import flask_sqlalchemy
import flask_migrate
from .settings import main_app


main_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'



DATABASE = flask_sqlalchemy.SQLAlchemy(app= main_app)

migrate = flask_migrate.Migrate(
    app = main_app,
    db = DATABASE,
    directory= "project/migrations"
)

