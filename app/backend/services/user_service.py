# services/user_service.py
from config import db
import bcrypt

def create_user(data):
    """Crea un usuario en la base de datos."""
    username = data.get("username")
    if db.users.find_one({"username": username}):
        return {"message": "El usuario ya existe"}, 409

    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    permissions = ["acceder_archivos", "subir_archivos"] if data["role"] == "Empleado" else ["crear_trabajadores", "acceder_papelera"]

    db.users.insert_one({
        "name": data["name"],
        "username": username,
        "password": hashed_password,
        "role": data["role"],
        "permissions": permissions
    })
    return {"message": f"{data['role']} creado exitosamente!"}, 201
