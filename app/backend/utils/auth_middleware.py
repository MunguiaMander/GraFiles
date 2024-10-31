# utils/auth_middleware.py
from functools import wraps
from flask import request, jsonify
import jwt
from config import SECRET_KEY, db

# Middleware de autenticación
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token es requerido!'}), 403
        try:
            token = token.split(" ")[1] 
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = data['username']
            # Recupera el usuario completo desde la base de datos
            current_user = db.users.find_one({"username": username})
            if not current_user:
                return jsonify({'message': 'Usuario no encontrado!'}), 403
        except Exception as e:
            return jsonify({'message': 'Token inválido!', 'error': str(e)}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# Middleware para verificar permisos específicos
def check_permissions(required_permissions):
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            user_permissions = current_user.get("permissions", [])
            if not all(permission in user_permissions for permission in required_permissions):
                return jsonify({'error': 'Permiso denegado!'}), 403
            return f(current_user, *args, **kwargs)
        return decorated_function
    return decorator
