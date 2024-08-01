from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User, user_schema, users_schema

bp = Blueprint('api', __name__)

def is_admin():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return user.role == UserRole.ADMIN

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 400
    
    new_user = User(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password']  # Note: Password should be hashed before storing
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.password == data['password']:  # Note: This should use proper password hashing
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"message": "Invalid credentials"}), 401

@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(user_schema.dump(user)), 200

@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    if not is_admin():
        return jsonify({"message": "Unauthorized"}), 403
    
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

@bp.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def user_operations(user_id):
    if not is_admin():
        return jsonify({"message": "Unauthorized"}), 403
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'GET':
        return jsonify(user_schema.dump(user)), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify(user_schema.dump(user)), 200
    
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200

@bp.route('/users/<int:user_id>/activate', methods=['PATCH'])
@jwt_required()
def activate_user(user_id):
    if not is_admin():
        return jsonify({"message": "Unauthorized"}), 403
    
    user = User.query.get_or_404(user_id)
    user.active = True
    db.session.commit()
    return jsonify({"message": "User activated successfully"}), 200

@bp.route('/users/<int:user_id>/deactivate', methods=['PATCH'])
@jwt_required()
def deactivate_user(user_id):
    if not is_admin():
        return jsonify({"message": "Unauthorized"}), 403
    
    user = User.query.get_or_404(user_id)
    user.active = False
    db.session.commit()
    return jsonify({"message": "User deactivated successfully"}), 200