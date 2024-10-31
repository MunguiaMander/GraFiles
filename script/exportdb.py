import json
import os
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['grafiles_db']

with open('db_script.js', 'w') as f:
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        data = list(collection.find({}))
        f.write(f"db.{collection_name}.insertMany({json.dumps(data, default=str)});\n")

print("Exportación completa.")
