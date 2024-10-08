import json
import os
from PySide6.QtWidgets import QMessageBox

DATABASE_PATH = 'sistemaOperativo/data/dataBaseUser/users.json'

def load_user_database():
    """Cargar la base de datos de usuarios desde el archivo JSON."""
    if os.path.exists(DATABASE_PATH):
        with open(DATABASE_PATH, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_user_database(user_database):
    """Guardar la base de datos de usuarios en un archivo JSON."""
    with open(DATABASE_PATH, 'w') as file:
        json.dump(user_database, file, indent=4)

