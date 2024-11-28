from app import create_app, db
from flask_migrate import MigrateCommand
from flask.cli import FlaskGroup

app = create_app()
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
