# routes/email_verification.py
from flask import Blueprint, request, jsonify
from flask_mail import Mail, Message
from flask_jwt_extended import create_access_token, decode_token
from models import db, User
from config import Config

email_verification_bp = Blueprint('email_verification', __name__)
mail = Mail()

def send_verification_email(user):
    token = create_access_token(identity=user.id)
    msg = Message("Verify Your Email", recipients=[user.email])
    msg.body = f"Please click the following link to verify your email: http://localhost:5000/auth/verify/{token}"
    mail.send(msg)

@email_verification_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@email_verification_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        user_id = decode_token(token)['sub']
        user = User.query.get(user_id)
        if user:
            user.verified = True  # Ensure you have a 'verified' field in your User model
            db.session.commit()
            return jsonify(message="Email verified successfully"), 200
    except:
        return jsonify(message="Verification link is invalid or has expired"), 400
