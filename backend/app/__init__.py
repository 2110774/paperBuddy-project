from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from loguru import logger
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_name='development'):
    app = Flask(__name__)

    # Load config
    from config import config
    app.config.from_object(config[config_name])

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # CORS - allow all origins in dev
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.students import students_bp
    from app.routes.scholarships import scholarships_bp
    from app.routes.applications import applications_bp
    from app.routes.ai_routes import ai_bp
    from app.routes.documents import documents_bp
    from app.routes.donations import donations_bp
    from app.routes.admin import admin_bp
    from app.routes.notifications import notifications_bp
    from app.routes.schools import schools_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(scholarships_bp, url_prefix='/api/scholarships')
    app.register_blueprint(applications_bp, url_prefix='/api/applications')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(documents_bp, url_prefix='/api/documents')
    app.register_blueprint(donations_bp, url_prefix='/api/donations')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    app.register_blueprint(schools_bp, url_prefix='/api/schools')

    # Health check
    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'message': 'EduBridge AI API is running'}

    logger.info("EduBridge AI Flask app initialized")
    return app
