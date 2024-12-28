from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets

# Initialize extensions
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shipping.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Security configuration
    app.config['SECRET_KEY'] = secrets.token_hex(16)

    # Override config with test config if provided
    if test_config is not None:
        app.config.update(test_config)

    # Initialize Flask extensions
    db.init_app(app)

    with app.app_context():
        # Import models
        from app.models import shipping
        from app.models.model_setup import setup_models
        
        # Setup models and create tables
        setup_models()

        # Register blueprints
        from app.routes import main
        app.register_blueprint(main.bp)

        from app.routes.crud import bp as crud_bp
        app.register_blueprint(crud_bp, url_prefix='/crud')

        # Configure context processors
        @app.context_processor
        def utility_processor():
            return dict(year=datetime.now().year)

        # Configure error handlers
        @app.errorhandler(404)
        def not_found_error(error):
            return render_template('404.html'), 404

        @app.errorhandler(500)
        def internal_error(error):
            db.session.rollback()
            return render_template('500.html'), 500

    return app
