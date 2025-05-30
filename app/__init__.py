# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    # Specify .env file path
    env_path = 'C:\\Users\\More\\Desktop\\siraj\\restaurants_menu_project\\hotel_menu_backend\\.env'
    if not os.path.exists(env_path):
        raise FileNotFoundError(f".env file not found at {env_path}")
    load_dotenv(env_path, override=True)

    # Load configuration
    # app.config.from_pyfile('config.py')  # Comment out to avoid conflicts
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Debug configuration
    print("SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    print("JWT_SECRET_KEY:", app.config['JWT_SECRET_KEY'])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.categories import categories_bp
    from app.routes.menu_items import menu_items_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(menu_items_bp)

    # Create database tables and default admin user
    with app.app_context():
        db.create_all()
        from app.models.user import User
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password='admin123', is_admin=True)
            db.session.add(admin)
            db.session.commit()
            print("Created admin user")

    return app