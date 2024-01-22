from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from extension import db
from app.models.User import User

server_bp = Blueprint('server', __name__)

# Endpoint đăng ký người dùng
@server_bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()

    new_user = User(UserName=data['username'], Email=data['email'], PassWord=data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Endpoint đăng nhập và trả về token
@server_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(UserName=username, PassWord=password).first()

    if user:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Các endpoint bảo vệ đòi hỏi xác thực JWT
@server_bp.route('/user', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    user_list = [{'UserID': user.UserID, 'UserName': user.UserName, 'Email': user.Email, 'Password': user.PassWord} for user in users]
    return jsonify({'users': user_list})

@server_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)

    if user:
        user_info = {'UserID': user.UserID, 'UserName': user.UserName, 'Email': user.Email, 'Password': user.PassWord}
        return jsonify({'user': user_info})
    
    return jsonify({'message': 'User not found'}), 404

@server_bp.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)

    if user:
        data = request.get_json()
        user.UserName = data.get('username', user.UserName)
        user.Email = data.get('email', user.Email)
        user.PassWord = data.get('password', user.PassWord)

        db.session.commit()

        return jsonify({'message': 'User updated successfully'})

    return jsonify({'message': 'User not found'}), 404

@server_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})

    return jsonify({'message': 'User not found'}), 404
