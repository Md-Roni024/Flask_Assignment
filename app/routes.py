from flask import jsonify, request
from app import db
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def register_routes(app):

    # @app.route('/')
    # def home():
    #     return "Welcome to the API! Use /register to create an account, /signin to log in, /reset-password to reset your password, and /users to manage users."

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        role = data.get('role', 'User')
        active = data.get('active', True)

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return jsonify({"msg": "Username or Email already exists"}), 400

        user = User(username=username, first_name=first_name, last_name=last_name, 
                    email=email, role=role, active=active)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.username)
        user_data = user_schema.dump(user)

        return jsonify({"msg": "User registered successfully!", "user": user_data, "access_token": access_token}), 201

    @app.route('/signin', methods=['POST'])
    def signin():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return jsonify({"msg": "Login successful"}), 200
        return jsonify({"msg": "Username or Password does not match"}), 401

    
    @app.route('/reset-password', methods=['PUT'])
    @jwt_required()
    def reset_password():
        data = request.get_json()
        username = data.get('username')
        new_password = data.get('new_password')
        current_password = data.get('current_password')

        current_user = User.query.filter_by(username=get_jwt_identity()).first()

        if current_user:
            # Admin can reset any user's password
            if current_user.role == 'Admin' and username:
                user = User.query.filter_by(username=username).first()
                if user:
                    user.set_password(new_password)
                    db.session.commit()
                    return jsonify({"msg": "Password reset successfully for user."}), 200
                return jsonify({"msg": "User not found"}), 404
            
            # Regular user resetting their own password
            if not current_password or not current_user.check_password(current_password):
                return jsonify({"msg": "Current password is incorrect"}), 401

            current_user.set_password(new_password)
            db.session.commit()
            return jsonify({"msg": "Password reset successfully!"}), 200

        return jsonify({"msg": "Unauthorized access"}), 403

    @app.route('/users', methods=['GET'])
    @jwt_required()
    def get_users():
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.role != 'Admin':
            return jsonify({"msg": "Unauthorized access"}), 403

        users = User.query.all()
        return jsonify(users_schema.dump(users))

    @app.route('/users/<int:user_id>', methods=['GET'])
    @jwt_required()
    def get_user(user_id):
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.role != 'Admin':
            return jsonify({"msg": "Unauthorized access"}), 403

        user = User.query.get(user_id)
        if user:
            return jsonify(user_schema.dump(user))
        return jsonify({"msg": "User not found"}), 404

    @app.route('/users/<int:user_id>', methods=['PUT'])
    @jwt_required()
    def update_user(user_id):
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.role != 'Admin' and current_user.id != user_id:
            return jsonify({"msg": "Unauthorized access"}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        data = request.get_json()
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.active = data.get('active', user.active)

        if current_user.role == 'Admin':
            user.role = data.get('role', user.role)

        db.session.commit()
        return jsonify({"msg": "User updated successfully"}), 200

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    @jwt_required()
    def delete_user(user_id):
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if current_user.role != 'Admin':
            return jsonify({"msg": "Unauthorized access"}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User deleted successfully"}), 200
