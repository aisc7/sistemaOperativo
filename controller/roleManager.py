import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QHBoxLayout, QMessageBox
)

DATABASE_PATH = './data/dataBaseUser/users.json'


class RoleManager:
    def __init__(self, users_file=DATABASE_PATH):
        self.users_file = users_file
        self.users_data = self.load_users_data()
        self.current_user = None  # Usuario actualmente autenticado

    def load_users_data(self):
        """Carga los datos de los usuarios desde el archivo JSON."""
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                return json.load(f)
        return {}

    def save_users_data(self):
        """Guarda los datos de los usuarios en el archivo JSON."""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        with open(self.users_file, "w") as f:
            json.dump(self.users_data, f, indent=4)

    def login(self, username, password):
        """Autentica un usuario y establece la sesión actual."""
        if username in self.users_data:
            user = self.users_data[username]
            if user["password"] == password:
                self.current_user = user
                return True, f"Bienvenido, {username}."
            return False, "Contraseña incorrecta."
        return False, "Usuario no encontrado."

    def logout(self):
        """Cierra la sesión actual."""
        self.current_user = None

    def is_admin(self):
        """Verifica si el usuario actual es administrador."""
        if self.current_user:
            return self.current_user.get("role", "").lower() == "administrator"
        return False

    def add_user(self, username, password="default", role="user"):
        """Agrega un nuevo usuario al sistema."""
        
        # Si es el primer usuario, asignamos el rol 'Administrator'
        if len(self.users_data) == 0:
            role = "Administrator"
        
        # Verificar si el usuario ya existe
        if username in self.users_data:
            return False, f"El usuario '{username}' ya existe."
        
        # Agregar al usuario
        self.users_data[username] = {
            "id": str(self.get_next_user_id()),
            "password": password,
            "role": role
        }
        self.save_users_data()
        
        # Si es el primer usuario, informamos que es el administrador
        if role == "Administrator":
            return True, f"Usuario '{username}' creado como Administrador."
        else:
            return True, f"Usuario '{username}' creado con éxito."

    def delete_user(self, username):
        """Elimina un usuario del sistema."""
        if username in self.users_data:
            del self.users_data[username]
            self.save_users_data()
            return True, f"Usuario '{username}' eliminado con éxito."
        return False, f"Usuario '{username}' no encontrado."

    def get_next_user_id(self):
        """Obtiene el próximo ID de usuario disponible."""
        if not self.users_data:
            return 1
        return max(int(user["id"]) for user in self.users_data.values()) + 1


class UserManagementWindow(QWidget):
    def __init__(self, parent=None):
        super(UserManagementWindow, self).__init__(parent)

        self.role_manager = RoleManager()

        # Verificar si el usuario actual es administrador
        if not self.role_manager.is_admin():
            QMessageBox.critical(self, "Acceso Denegado", "No tienes permisos para acceder a esta ventana.")
            self.close()
            return

        self.setWindowTitle("Manage Users and Roles")
        self.setStyleSheet("background-color: #3B4252; color: white;")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()

        title = QLabel("Manage Users and Roles")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")

        # Tabla para mostrar usuarios
        self.user_table = QTableWidget(0, 2)
        self.user_table.setHorizontalHeaderLabels(["Username", "Role"])
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.refresh_table()

        # Controles para añadir/actualizar usuarios
        controls_layout = QHBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setStyleSheet("padding: 5px;")

        self.role_selector = QComboBox()
        self.role_selector.addItems(["Admin", "Editor", "Viewer"])
        self.role_selector.setStyleSheet("padding: 5px;")

        self.add_user_button = QPushButton("Add/Update User")
        self.add_user_button.setStyleSheet(self.get_button_style())
        self.add_user_button.clicked.connect(self.add_or_update_user)

        controls_layout.addWidget(self.username_input)
        controls_layout.addWidget(self.role_selector)
        controls_layout.addWidget(self.add_user_button)

        # Botón para eliminar usuarios
        self.delete_user_button = QPushButton("Delete Selected User")
        self.delete_user_button.setStyleSheet(self.get_button_style())
        self.delete_user_button.clicked.connect(self.delete_user)

        layout.addWidget(title)
        layout.addWidget(self.user_table)
        layout.addLayout(controls_layout)
        layout.addWidget(self.delete_user_button)

        self.setLayout(layout)

    def get_button_style(self):
        """Estilo para los botones."""
        return """
            QPushButton {
                background-color: #5E81AC;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """

    def refresh_table(self):
        """Llena la tabla con los datos actuales."""
        self.user_table.setRowCount(0)
        for username, data in self.role_manager.users_data.items():
            row_position = self.user_table.rowCount()
            self.user_table.insertRow(row_position)
            self.user_table.setItem(row_position, 0, QTableWidgetItem(username))
            self.user_table.setItem(row_position, 1, QTableWidgetItem(data["role"]))

    def add_or_update_user(self):
        """Añadir o actualizar un usuario."""
        username = self.username_input.text().strip()
        role = self.role_selector.currentText()

        if username:
            # Verificar si el usuario actual es administrador antes de cambiar el rol
            if not self.role_manager.is_admin() and role != "user":
                QMessageBox.warning(self, "Acceso Denegado", "Solo los administradores pueden cambiar el rol de otros usuarios.")
                return
            
            success, message = self.role_manager.add_user(username, role=role)
            QMessageBox.information(self, "Info", message)
            self.refresh_table()
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un nombre de usuario válido.")

    def delete_user(self):
        """Eliminar el usuario seleccionado."""
        selected_row = self.user_table.currentRow()
        if selected_row >= 0:
            username = self.user_table.item(selected_row, 0).text()
            success, message = self.role_manager.delete_user(username)
            QMessageBox.information(self, "Info", message)
            self.refresh_table()
        else:
            QMessageBox.warning(self, "Error", "Por favor, seleccione un usuario para eliminar.")
