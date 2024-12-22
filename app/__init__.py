from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import click

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main.bp)
    
    # Ensure the instance folder exists
    try:
        import os
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register CLI commands
    @app.cli.command("init-db")
    def init_db():
        """Initialize the database."""
        click.echo('Creating database tables...')
        db.create_all()
        click.echo('Database tables created!')

    @app.cli.command("seed-db")
    def seed_db():
        """Seed the database with initial data."""
        from app.models.shipping import (
            Country, Port, ShippingCompany, 
            ContainerStatus, PackType, Commodity
        )

        # Add some initial data
        if not Country.query.first():
            countries = [
                Country(name='United States'),
                Country(name='China'),
                Country(name='Singapore')
            ]
            db.session.add_all(countries)
            db.session.commit()
            click.echo('Added initial countries')

        if not ContainerStatus.query.first():
            statuses = [
                ContainerStatus(name='Empty', description='Container is empty'),
                ContainerStatus(name='Loaded', description='Container is loaded'),
                ContainerStatus(name='In Transit', description='Container is in transit')
            ]
            db.session.add_all(statuses)
            db.session.commit()
            click.echo('Added container statuses')

        click.echo('Database seeded!')
        
    return app
