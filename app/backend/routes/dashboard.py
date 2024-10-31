# routes/dashboard.py
from flask import Blueprint, jsonify, request
from utils.auth_middleware import token_required, check_permissions
from models.file_model import FileModel
from models.user_model import UserModel

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard(current_user):
    """Obtiene los archivos del usuario autenticado y su rol."""
    files = FileModel.get_files_by_user(current_user["username"])
    return jsonify({
        "files": files,
        "role": current_user.get("role"),
        "name": current_user.get("name")
    })

@dashboard_bp.route('/add_test_files', methods=['GET'])
def add_test_files():
    """Endpoint para agregar archivos de prueba (solo para desarrollo)."""
    result = FileModel.create_test_files()
    return jsonify(result), 200

@dashboard_bp.route('/create_user', methods=['POST'])
@token_required
@check_permissions(['crear_trabajadores'])
def create_user(current_user):
    """Crea un nuevo usuario en la base de datos (solo para administradores)."""
    data = request.get_json()
    result, status = UserModel.create_user(data)
    return jsonify(result), status