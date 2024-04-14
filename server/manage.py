from flask.cli import FlaskGroup
from flask_migrate import Migrate
from app import app, db  # Assuming your Flask app instance is named "app" and your database instance is named "db"

# Import models (assuming your models are in a file called models.py)
from models import *

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Create a custom CLI command group
cli = FlaskGroup(app)

# Add Flask-Migrate commands to the custom CLI group
cli.add_command('db')

if __name__ == '__main__':
    cli()
