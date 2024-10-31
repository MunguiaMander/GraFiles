# routes/auth.py
from flask import Blueprint, request, jsonify
import jwt
import bcrypt
from datetime import datetime, timedelta
from config import db, SECRET_KEY

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    if password != confirm_password:
        return jsonify({"message": "Las contraseñas no coinciden"}), 400
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.users.insert_one({
        "username": username,
        "password": hashed_password,
        "role": "Administrador",
        "permissions": ["crear_trabajadores", "acceder_papelera"]
    })

    return jsonify({"message": "Administrador registrado exitosamente!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = db.users.find_one({"username": username})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        return jsonify({"message": "Usuario o contraseña incorrectos"}), 401
    token = jwt.encode(
        {"username": user["username"], "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return jsonify({"token": token})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Sesión cerrada"}), 200
