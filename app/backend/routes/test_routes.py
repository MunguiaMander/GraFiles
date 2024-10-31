from flask import Blueprint, jsonify
from config import db

test_bp = Blueprint('test_routes', __name__)

@test_bp.route('/files/shared_test', methods=['GET'])
def get_shared_files_test():
    try:
        # Obtener todos los archivos en la colección "shared"
        shared_files = db.shared.find()
        files = []

        for file in shared_files:
            files.append({
                "_id": str(file["_id"]),
                "filename": file.get("filename"),
                "description": file.get("description", "Sin descripción"),
                "extension": file.get("extension", "unknown"),
                "owner": file.get("original_author", "Desconocido"),
                "shared_with": file.get("shared_with", "Desconocido"),
                "shared_at": file.get("shared_at")
            })
        
        return jsonify(files), 200
    
    except Exception as e:
        print("Error al obtener archivos compartidos:", e)
        return jsonify({"message": "Error al obtener archivos compartidos"}), 500

@test_bp.route('/files/thrashed_test', methods=['GET'])
def get_thrashed_files_test():
    try:
        # Obtener todos los archivos en la colección "thrashed"
        thrashed_files = db.thrashed.find()
        files = []

        for file in thrashed_files:
            files.append({
                "_id": str(file["_id"]),
                "filename": file.get("filename"),
                "description": file.get("description", "Sin descripción"),
                "extension": file.get("extension", "unknown"),
                "owner": file.get("owner", "Desconocido"),
                "directory": file.get("directory", "/mis_archivos"),
                "status": file.get("status", "unknown"),
                "created_at": file.get("created_at")
            })
        
        return jsonify(files), 200

    except Exception as e:
        print("Error al obtener archivos eliminados:", e)
        return jsonify({"message": "Error al obtener archivos eliminados"}), 500
