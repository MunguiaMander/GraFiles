# models/user_model.py
from config import db
import bcrypt

class UserModel:
    @staticmethod
    def create_user(data):
        """Crea un nuevo usuario en la base de datos."""
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

    @staticmethod
    def get_user_permissions(username):
        """Obtiene los permisos de un usuario específico."""
        user = db.users.find_one({"username": username}, {"permissions": 1})
        return user.get("permissions", []) if user else []
