# routes/user_profile.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User

user_profile_bp = Blueprint('user_profile', __name__)

@user_profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify(message="Invalid token"), 422

    user = User.query.get(current_user)
    if user:
        return jsonify(username=user.username, email=user.email), 200
    return jsonify(message="User not found"), 404

@user_profile_bp.route('/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    if user:
        username = data.get('username')
        email = data.get('email')

        if username:
            user.username = username
        if email:
            user.email = email

        db.session.commit()
        return jsonify(message="Profile updated successfully"), 200
    return jsonify(message="User not found"), 404

@user_profile_bp.route('/profile/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    if user and user.check_password(data.get('old_password')):
        user.set_password(data.get('new_password'))
        db.session.commit()
        return jsonify(message="Password updated successfully"), 200
    return jsonify(message="Old password is incorrect"), 401
