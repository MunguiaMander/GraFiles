# config.py
from pymongo import MongoClient
import os

# Configuración de la base de datos
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client['grafiles_db']

# Configuración JWT
SECRET_KEY = os.environ.get("SECRET_KEY", "salt")

class Config:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')