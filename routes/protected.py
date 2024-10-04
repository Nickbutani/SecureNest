from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from role_required import role_required

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/admin', methods=['GET'])
@jwt_required()
@role_required('admin')
def dashboard():
    return jsonify({"message": "Welcome to the protected dashboard"}), 200
