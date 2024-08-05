from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    with app.app_context():
        # Import the models to ensure they are registered
        from .models import User  # Ensure all models are imported here
        db.create_all()

    from .routes import userBlueprint
    app.register_blueprint(userBlueprint)

    # Swagger UI setup
    # swagger_url = '/swagger'
    # api_url = '/static/swagger.json'
    # swagger_ui_bp = get_swaggerui_blueprint(
    #     swagger_url,
    #     api_url,
    #     config={
    #         'app_name': "Flask API"
    #     }
    # )
    # app.register_blueprint(swagger_ui_bp, url_prefix=swagger_url)

    return app
