# services/file_service.py
from config import db
from datetime import datetime

def get_files_by_user(username):
    """Obtiene los archivos activos del usuario especificado."""
    files = db.files.find({"owner": username, "status": "active"})
    return [
        {
            "filename": f["filename"],
            "directory": f["directory"],
            "description": f.get("description", "Sin descripción"),
            "extension": f["filename"].split('.')[-1],
            "owner": f["owner"]
        }
        for f in files
    ]

def add_test_files():
    """Añade archivos de prueba a la base de datos."""
    test_files = [
        {"filename": "documento1.txt", "directory": "/mis_archivos", "owner": "admin", "status": "active"},
        {"filename": "imagen1.png", "directory": "/imagenes", "owner": "admin", "status": "active"},
        {"filename": "documento_eliminado.txt", "directory": "/mis_archivos", "owner": "admin", "status": "trashed", "deleted_at": datetime.utcnow()}
    ]
    db.files.insert_many(test_files)
    return {"message": "Archivos de prueba añadidos exitosamente!"}

# services/file_service.py
from config import db

def save_image_file(filename, owner, directory, description, extension="image"):
    file_data = {
        "filename": filename,
        "owner": owner,
        "directory": directory,
        "description": description,
        "extension": extension,
        "status": "active",
    }
    db.files.insert_one(file_data)
    return file_data

def insert_test_image():
    """Inserta una imagen de prueba en la colección de files."""
    file_data = {
        "filename": "imagen12.png",
        "owner": "admin",
        "directory": "/uploads",
        "description": "Imagen de prueba",
        "extension": "png",
        "type": "image",
        "status": "active",
        "created_at": datetime.utcnow()
    }
    result = db.files.insert_one(file_data)
    print(f"Imagen de prueba insertada con ID: {result.inserted_id}")