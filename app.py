from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from urllib.parse import quote

app = Flask(__name__)

# URL encode your password if it contains special characters
password = 'p@stgress'
encoded_password = quote(password)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{encoded_password}@localhost:5433/hotel_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '173120'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Enum('Admin', 'User', name='user_roles'), default='User')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.before_request
def create_tables():
    # only run on the first request
    app.before_request_funcs[None].remove(create_tables)

    db.create_all()


@app.route('/')
def home():
    return "This is my Home route!"

@app.route('/test-db')
def test_db_connection():
    try:
        result = db.session.execute(text('SELECT 1'))
        return jsonify({"msg": "Database connected successfully!", "result": [row[0] for row in result]}), 200
    except Exception as e:
        return jsonify({"msg": "Database connection failed.", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
