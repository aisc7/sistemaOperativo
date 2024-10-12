import json
import os
from PySide6.QtWidgets import QMessageBox

DATABASE_PATH = './data/dataBaseUser/users.json'

def load_user_database():
    """Cargar la base de datos de usuarios desde el archivo JSON."""
    if os.path.exists(DATABASE_PATH):
        with open(DATABASE_PATH, 'r') as file:
            content = file.read().strip()  # Leer el contenido y eliminar espacios en blanco
            if content:  # Si hay contenido en el archivo
                user_database = json.loads(content)  # Cargar el JSON
                # Obtener el primer usuario (la primera clave del diccionario)
                first_user = next(iter(user_database)) if user_database else None
                return user_database, first_user  # Retorna el diccionario y el primer usuario
            else:
                return {}, None  # Retornar un diccionario vacío y None si el archivo está vacío
    else:
        return {}, None  # Retornar un diccionario vacío y None si el archivo no existe

def save_user_database(user_database):
    """Guardar la base de datos de usuarios en un archivo JSON."""
    # Asegurarse de que el directorio exista
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    with open(DATABASE_PATH, 'w') as file:
        json.dump(user_database, file, indent=4)
