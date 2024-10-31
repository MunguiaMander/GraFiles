# routes/file_routes.py
from datetime import datetime
import os
from bson import ObjectId
from flask import Blueprint, current_app, jsonify, request
from utils.auth_middleware import token_required
from werkzeug.utils import secure_filename
from services.file_service import get_files_by_user, add_test_files, save_image_file
from models.file_model import FileModel
from config import db


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../frontend/static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

file_bp = Blueprint('file_routes', __name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@file_bp.route('/dashboard', methods=['GET'])
@token_required
def get_files(current_user):
    files = get_files_by_user(current_user["username"])
    return jsonify({
        "files": files,
        "role": current_user.get("role"),
        "name": current_user.get("name")
    })

@file_bp.route('/add_test_files', methods=['GET'])
def add_files():
    return jsonify(add_test_files()), 200


@file_bp.route('/create_txt', methods=['POST'])
@token_required
def create_txt(current_user):
    data = request.get_json()
    filename = data.get('filename')
    description = data.get('description', "Sin descripción")
    content = data.get('content')

    if not filename or not content:
        return jsonify({"message": "El nombre del archivo y el contenido son obligatorios"}), 400
    result = FileModel.create_file(filename=filename, owner=current_user['username'], directory="/mis_archivos", content=content, description=description)
    result['_id'] = str(result['_id'])  

    return jsonify(result), 201


@file_bp.route('/upload_image', methods=['POST'])
@token_required
def upload_image(current_user):
    try:
        file = request.files['image']
        description = request.form.get('description', "Sin descripción")

        directory = 'app/frontend/static/uploads'
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = file.filename
        filepath = os.path.join(directory, filename)
        file.save(filepath)
        file_data = {
            "filename": filename,
            "owner": current_user["username"],
            "directory": f"/uploads",  
            "description": description,
            "extension": filename.split('.')[-1],
            "status": "active",
            "created_at": datetime.utcnow()
        }
        result = db.files.insert_one(file_data)

        file_data["_id"] = str(result.inserted_id)

        return jsonify({"message": "Imagen subida exitosamente", "file": file_data}), 201

    except Exception as e:
        print("Error en la subida de imagen:", str(e))
        return jsonify({"message": "Error inesperado al subir la imagen", "error": str(e)}), 500


@file_bp.route('/insert_test_image', methods=['GET'])
def insert_test_image_endpoint():
    from services.file_service import insert_test_image
    insert_test_image()
    return jsonify({"message": "Imagen de prueba insertada exitosamente"}), 201

from bson import ObjectId, errors
from flask import jsonify

@file_bp.route('/<file_id>', methods=['GET'])
@token_required
def get_file_details(current_user, file_id):
    try:
        if not ObjectId.is_valid(file_id):
            return jsonify({"message": "ID de archivo no válido"}), 400

        # Listas de colecciones donde se buscará el archivo
        collections = [db.files, db.trashed, db.shared]
        file_data = None
        for collection in collections:
            file_data = collection.find_one({"_id": ObjectId(file_id)})
            if file_data:
                file_data["_id"] = str(file_data["_id"])  
                return jsonify(file_data), 200

        return jsonify({"message": "Archivo no encontrado"}), 404

    except errors.InvalidId:
        return jsonify({"message": "Formato de ID no válido"}), 400
    except Exception as e:
        print("Error al obtener detalles del archivo:", e)
        return jsonify({"message": "Error al obtener detalles del archivo"}), 500


@file_bp.route('/upload_txt', methods=['POST'])
@token_required
def upload_txt_file(current_user):
    try:
        if 'file' not in request.files:
            return jsonify({"message": "No se encontró el archivo"}), 400

        file = request.files['file']
        description = request.form.get('description', "Sin descripción")
        if file.filename.split('.')[-1].lower() != 'txt':
            return jsonify({"message": "Formato de archivo no soportado. Solo se permiten archivos TXT."}), 400
        content = file.read().decode('utf-8')
        file_data = {
            "filename": file.filename,
            "owner": current_user["username"],
            "directory": "/mis_archivos", 
            "description": description,
            "extension": "txt",
            "type": "txt",
            "content": content,
            "status": "active",
            "created_at": datetime.utcnow()
        }
        db.files.insert_one(file_data)
        return jsonify({"message": "Archivo TXT subido exitosamente"}), 201

    except Exception as e:
        print(f"Error al subir el archivo TXT: {e}")
        return jsonify({"message": "Error al procesar el archivo"}), 500

@file_bp.route('/delete/<file_id>', methods=['DELETE'])
@token_required
def delete_file(current_user, file_id):
    file = db.files.find_one({"_id": ObjectId(file_id)})
    if not file:
        return jsonify({"message": "Archivo no encontrado"}), 404

    # Insertar el archivo en la colección `thrashed`
    db.thrashed.insert_one(file)
    db.files.delete_one({"_id": ObjectId(file_id)})

    return jsonify({"message": "Archivo movido a la papelera"}), 200


@file_bp.route('/share', methods=['POST'])
@token_required
def share_file(current_user):
    data = request.get_json()
    file_id = data.get("fileId")
    users = data.get("users", [])

    if not file_id or not users:
        return jsonify({"message": "Faltan datos para compartir el archivo"}), 400

    try:
        # Busca el archivo original en la colección de archivos
        original_file = db.files.find_one({"_id": ObjectId(file_id)})
        
        if not original_file:
            return jsonify({"message": "Archivo no encontrado"}), 404

        # Crea una copia del archivo para cada usuario seleccionado en la colección `shared`
        for username in users:
            shared_file = original_file.copy() 
            shared_file.update({
                "shared_with": username,
                "original_author": current_user["username"],
                "shared_at": datetime.utcnow(),
                "status": "shared"
            })
            db.shared.insert_one(shared_file) 

        return jsonify({"message": "Archivo compartido exitosamente"}), 200

    except Exception as e:
        print("Error al compartir archivo:", e)
        return jsonify({"message": "Error al compartir el archivo"}), 500

@file_bp.route('/files/shared', methods=['GET'])
@token_required
def get_shared_files(current_user):
    try:
        # Filtra solo los archivos compartidos con el usuario actual
        files = db.shared.find({"shared_with": current_user["username"]})
        shared_files = [{
            "_id": str(file["_id"]),
            "filename": file["filename"],
            "description": file.get("description", "Sin descripción"),
            "extension": file["extension"],
            "owner": file["original_author"],
            "directory": file["directory"] 
        } for file in files]
        
        return jsonify(shared_files), 200
    except Exception as e:
        print("Error al obtener archivos compartidos:", e)
        return jsonify({"message": "Error al obtener archivos compartidos"}), 500
