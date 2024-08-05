from flask import Blueprint, request, url_for,jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from .schemas import UserSchema, UserRegistrationSchema, UserLoginSchema,UpdateUserSchema
from .utils import generate_token
from config import Config
from marshmallow import ValidationError

userBlueprint = Blueprint("user", __name__, url_prefix="/")

user_schema = UserSchema()
user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()


#Route-1: Home Route or Root Route
@userBlueprint.route("/",methods=['GET'])
def home():
    return "Home Route"


#Route-2: User Registration Route
@userBlueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("data:", data)
    try:
        user_data = user_registration_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    if User.query.filter_by(username=user_data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=user_data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    # Directly use the role from user input
    role = user_data.get('role', 'User')  # Default to 'User' if not provided

    user = User(
        username=user_data['username'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        email=user_data['email'],
        role=user_data.get('role', 'USER').upper(),
        active=user_data.get('active', True)
    )
    user.set_password(user_data['password'])

    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "message": "User created",
        "user": user.to_dict()
    }), 201



#Route-3: Get All Users Route
@userBlueprint.route('/users', methods=['GET'])
# @jwt_required()
def get_all_users():

    # current_user = User.query.filter_by(username=get_jwt_identity()).first()
    # print("Current User:",current_user)
    # if current_user.role != 'ADMIN':
    #     return jsonify({"msg": "Unauthorized access"}), 403

    users = User.query.all()
    data = []

    for user in users:
        data.append({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role': user.role,
            'created_date': user.created_date,
            'updated_date': user.updated_date,
            'active': user.active
        })

    return jsonify({
        "message": "All Users",
        "user": data
    }), 200



#Route-4: Get single user by ID Route
@userBlueprint.route('/users/<int:user_id>', methods=['GET'])
# @jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "Message":"User by user id",
        "user":user.to_dict()
    }),200




#Route-5: Delete User by ID Route
@userBlueprint.route('/users/<int:user_id>', methods=['DELETE'])
# @jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    print("User Will Delete:",user)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"}), 200

@userBlueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = user_login_schema.validate(data)
    if errors:
        return jsonify({
            "Message":"Username or Password not validate",
        }),400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({
            "Message":"Invalid credentials"
        }),401
    
    access_token = generate_token(user)
    return jsonify({
        "Message":"Login Successful",
        "Token":access_token
    })




#Route-6: Update User by username
@userBlueprint.route('/update_profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()


    update_schema = UpdateUserSchema()

    try:
        validated_data = update_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # Update user information
    if 'first_name' in validated_data:
        user.first_name = validated_data['first_name']
    if 'last_name' in validated_data:
        user.last_name = validated_data['last_name']
    if 'email' in validated_data:
        if User.query.filter(User.email == validated_data['email'], User.id != user.id).first():
            return jsonify({"error": "Email already exists"}), 400
        user.email = validated_data['email']

    # Handle password update
    if 'current_password' in validated_data and 'new_password' in validated_data:
        if not user.check_password(validated_data['current_password']):
            return jsonify({"error": "Current password is incorrect"}), 400
        user.set_password(validated_data['new_password'])

    # Commit the changes to the database
    db.session.commit()

    return jsonify({
        "message": "User information updated successfully",
        "user": user.to_dict()
    }), 200





# @userBlueprint.route('/reset-password-request', methods=['POST'])
# def reset_password_request():
#     data = request.get_json()
#     email = data.get('email')
#     user = User.query.filter_by(email=email).first()

#     if not user:
#         return response_with(404, error="User not found")

#     token_serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
#     token = token_serializer.dumps({'user_id': user.id}).decode('utf-8')
#     reset_link = url_for('userBlueprint.reset_password_confirm', token=token, _external=True)

#     send_email('Password Reset Request', email, f'Click the link to reset your password: {reset_link}')

#     return response_with(200, message="Password reset link sent")

# @userBlueprint.route('/reset-password-confirm/<token>', methods=['POST'])
# def reset_password_confirm(token):
#     token_serializer = Serializer(current_app.config['SECRET_KEY'])
#     try:
#         data = token_serializer.loads(token)
#     except Exception:
#         return response_with(400, error="Invalid or expired token")

#     user = User.query.get_or_404(data['user_id'])
#     data = request.get_json()
#     new_password = data.get('new_password')
#     if not new_password:
#         return response_with(400, error="New password is required")
    
#     user.set_password(new_password)
#     db.session.commit()
    
#     return response_with(200, message="Password updated successfully")
