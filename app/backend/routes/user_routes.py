# routes/user_routes.py
from flask import Blueprint, jsonify, request
from utils.auth_middleware import token_required, check_permissions
from services.user_service import create_user
from config import db


user_bp = Blueprint('user_routes', __name__)

@user_bp.route('/create_user', methods=['POST'])
@token_required
@check_permissions(['crear_trabajadores'])
def add_user(current_user):
    data = request.get_json()
    result, status = create_user(data)
    return jsonify(result), status

@user_bp.route('/users_list', methods=['GET'])
@token_required
def get_users(current_user):
    try:
        users = list(db.users.find({}, {"_id": 0, "username": 1}))
        user_list = [{"username": user["username"]} for user in users]

        print("Usuarios procesados:", user_list)
        return jsonify(user_list), 200
    except Exception as e:
        print("Error al obtener usuarios:", e)
        return jsonify({"message": "Error al obtener la lista de usuarios"}), 500

