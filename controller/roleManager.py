import json
import os

class RoleManager:
    def __init__(self, users_file="data/dataBaseUser/users.json", base_dir="data/users/"):
        self.users_file = users_file
        self.base_dir = base_dir
        self.users_data = self.load_users_data()

        # Crear directorio base si no existe
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def load_users_data(self):
        """Carga los datos de los usuarios desde el archivo JSON."""
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                data = json.load(f)
                return data.get("users", [])
        else:
            print("Archivo de usuarios no encontrado.")
            return []

    def save_users_data(self):
        """Guarda los datos de los usuarios en el archivo JSON."""
        with open(self.users_file, "w") as f:
            json.dump({"users": self.users_data}, f, indent=4)

    def make_admin(self, username):
        """Hacer que un usuario sea administrador."""
        for user in self.users_data:
            if user["username"] == username:
                user["role"] = "admin"
                self.save_users_data()
                print(f"{username} ahora es administrador.")
                return
        print(f"Usuario {username} no encontrado.")

    def revoke_admin(self, username):
        """Revocar el rol de administrador a un usuario."""
        for user in self.users_data:
            if user["username"] == username:
                user["role"] = "user"
                self.save_users_data()
                print(f"{username} ya no es administrador.")
                return
        print(f"Usuario {username} no encontrado.")

    def add_user(self, username, password):
        """Agregar un nuevo usuario y crear su directorio personal."""
        new_user = {
            "id": self.get_next_user_id(),  # Asignar ID automáticamente
            "username": username,
            "password": password,
            "role": "admin" if len(self.users_data) == 0 else "user"  # El primer usuario es admin
        }
        self.users_data.append(new_user)
        self.save_users_data()
        
        # Crear el directorio del usuario
        user_dir = os.path.join(self.base_dir, username)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
            print(f"Directorio creado para el usuario: {username}")
        
        print(f"Usuario {username} agregado con éxito.")

    def remove_user(self, username):
        """Eliminar un usuario y su directorio personal."""
        for user in self.users_data:
            if user["username"] == username:
                self.users_data.remove(user)
                self.save_users_data()
                
                # Eliminar el directorio del usuario
                user_dir = os.path.join(self.base_dir, username)
                if os.path.exists(user_dir):
                    os.rmdir(user_dir)
                    print(f"Directorio de {username} eliminado.")
                
                print(f"Usuario {username} eliminado con éxito.")
                return
        print(f"Usuario {username} no encontrado.")

    def display_users(self):
        """Mostrar todos los usuarios y sus roles."""
        for user in self.users_data:
            print(f"Username: {user['username']}, Role: {user['role']}")

    def get_next_user_id(self):
        """Obtiene el próximo ID de usuario disponible."""
        if not self.users_data:
            return 1  # Si no hay usuarios, el primer ID es 1
        return max(user["id"] for user in self.users_data) + 1  # Retorna el siguiente ID disponible
