from config import db
from datetime import datetime
from bson import ObjectId

class FileModel:
    # Método para guardar un archivo de texto en la base de datos
    @staticmethod
    def create_file(filename, owner, directory, content, description="Sin descripción", extension="txt", status="active"):

        if extension == "txt" and not filename.endswith(".txt"):
            filename = f"{filename}.txt"

        file_data = {
            "filename": filename,
            "owner": owner,
            "directory": directory,
            "content": content,
            "description": description,
            "extension": extension, 
            "status": status,
            "created_at": datetime.utcnow()
        }
        db.files.insert_one(file_data)
        return file_data

    @staticmethod
    def exists(owner, filename):

        return db.files.find_one({"owner": owner, "filename": filename}) is not None

    @staticmethod
    def get_files_by_user(username):

        files = db.files.find({"owner": username, "status": "active"})
        return [
            {
                "filename": f["filename"],
                "directory": f.get("directory", "/"),
                "description": f.get("description", "Sin descripción"),
                "extension": f["filename"].split('.')[-1],
                "type": f.get("type", "txt"),
                "content": f.get("content", "") if f.get("type") == "txt" and f.get("content") is not None else "",  
                "_id": str(f["_id"]), 
                "owner": f["owner"]
            }
            for f in files
        ]

    
    @staticmethod
    def create_image(filename, owner, path, description="Sin descripción"):
        file_data = {
            "filename": filename,
            "owner": owner,
            "path": path,
            "description": description,
            "extension": filename.split('.')[-1],
            "status": "active",
            "created_at": datetime.utcnow()
        }
        db.files.insert_one(file_data)
        return file_data

    @staticmethod
    def upload_image(filename, owner, directory, image_data, description="Sin descripción"):

        if FileModel.exists(owner, filename):
            return {"message": "La imagen ya existe"}, 409  

        file_data = {
            "filename": filename,
            "owner": owner,
            "directory": directory,
            "description": description,
            "type": "image",
            "status": "active",
            "created_at": datetime.utcnow(),
            "image_data": image_data  
        }

        result = db.files.insert_one(file_data)
        file_data["_id"] = str(result.inserted_id)

        print("Filename:", filename)
        print("Description:", description)
        print("Owner:", owner)  
        print("Image Data:", image_data) 
        return file_data
