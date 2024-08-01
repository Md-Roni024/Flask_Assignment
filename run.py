from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from app.config import Config
from app.models import db, ma
from app.routes import bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    app.register_blueprint(bp)

    return app

app = create_app()

@app.cli.command("create-tables")
def create_tables():
    db.create_all()
    print("Tables created successfully")

if __name__ == '__main__':
    app.run(debug=True)