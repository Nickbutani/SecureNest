# routes/password_reset.py
from flask import Blueprint, request, jsonify
from flask_mail import Mail, Message
from flask_jwt_extended import create_access_token, decode_token, jwt_required
from models import db, User

password_reset_bp = Blueprint('password_reset', __name__)
mail = Mail()

def send_password_reset_email(user, token):
    msg = Message("Reset Your Password", recipients=[user.email])
    msg.body = f"Click the link to reset your password: http://localhost:5000/auth/reset/{token}"
    mail.send(msg)

@password_reset_bp.route('/password-reset', methods=['POST'])
@jwt_required()
def password_reset():
    email = request.json.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        token = create_access_token(identity=user.id)
        send_password_reset_email(user, token)
        return jsonify(message="Password reset link sent"), 200
    return jsonify(message="Email not found"), 404

@password_reset_bp.route('/reset/<token>', methods=['PUT'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get('new_password')

    try:
        user_id = decode_token(token)['sub']
        user = User.query.get(user_id)
        if user:
            user.set_password(new_password)
            db.session.commit()
            return jsonify(message="Password has been reset"), 200
    except:
        return jsonify(message="Invalid or expired token"), 400
