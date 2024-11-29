import json
import platform
import psutil
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QComboBox
)

DATABASE_PATH = './data/dataBaseUser/users.json'


class AdminPanel(QWidget):
    def __init__(self, parent=None):
        super(AdminPanel, self).__init__(parent)

        self.setWindowTitle("Admin Panel")
        self.setStyleSheet("background-color: #3B4252; color: white;")
        self.setFixedSize(600, 400)

        self.layout = QVBoxLayout()

        # Título
        self.title_label = QLabel("Administration Panel")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")

        # Botones de administración
        self.manage_users_button = QPushButton("Manage Users and Roles")
        self.manage_users_button.setStyleSheet(self.get_button_style())
        self.manage_users_button.clicked.connect(self.manage_users)

        self.system_info_button = QPushButton("View System Info")
        self.system_info_button.setStyleSheet(self.get_button_style())
        self.system_info_button.clicked.connect(self.view_system_info)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.manage_users_button)
        self.layout.addWidget(self.system_info_button)

        self.setLayout(self.layout)

    def get_button_style(self):
        """Estilo común para los botones."""
        return """
            QPushButton {
                background-color: #4C566A;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """

    def manage_users(self):
        """Abrir la interfaz de gestión de usuarios."""
        self.user_management_window = UserManagementWindow(self)
        self.user_management_window.show()

    def view_system_info(self):
        """Abrir la ventana de información del sistema."""
        self.system_info_window = SystemInfoWindow(self)
        self.system_info_window.show()


class UserManagementWindow(QWidget):
    def __init__(self, parent=None):
        super(UserManagementWindow, self).__init__(parent)

        self.setWindowTitle("Manage Users and Roles")
        self.setStyleSheet("background-color: #3B4252; color: white;")
        self.setFixedSize(500, 400)

        # Cargar datos de usuarios
        self.user_data = self.load_user_data()

        layout = QVBoxLayout()

        title = QLabel("Manage Users and Roles")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")

        # Tabla para mostrar usuarios
        self.user_table = QTableWidget(len(self.user_data), 2)
        self.user_table.setHorizontalHeaderLabels(["Username", "Role"])
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.populate_table()

        # Añadir controles para gestionar usuarios
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

    def load_user_data(self):
        """Carga los datos del archivo JSON."""
        if os.path.exists(DATABASE_PATH):
            with open(DATABASE_PATH, 'r') as file:
                return json.load(file)
        return {}

    def save_user_data(self):
        """Guarda los datos en el archivo JSON."""
        with open(DATABASE_PATH, 'w') as file:
            json.dump(self.user_data, file, indent=4)

    def populate_table(self):
        """Llena la tabla con datos de usuarios."""
        for row, (username, data) in enumerate(self.user_data.items()):
            self.user_table.setItem(row, 0, QTableWidgetItem(username))
            self.user_table.setItem(row, 1, QTableWidgetItem(data['role']))

    def add_or_update_user(self):
        """Añadir o actualizar un usuario."""
        username = self.username_input.text().strip()
        role = self.role_selector.currentText()

        if username:
            if username in self.user_data:
                self.user_data[username]['role'] = role
                QMessageBox.information(self, "Update User", f"User '{username}' updated to role '{role}'.")
            else:
                self.user_data[username] = {'id': len(self.user_data) + 1, 'password': 'default', 'role': role}
                QMessageBox.information(self, "Add User", f"User '{username}' added with role '{role}'.")

            self.save_user_data()
            self.refresh_table()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid username.")

    def delete_user(self):
        """Eliminar el usuario seleccionado."""
        selected_row = self.user_table.currentRow()
        if selected_row >= 0:
            username = self.user_table.item(selected_row, 0).text()
            del self.user_data[username]
            self.save_user_data()
            self.refresh_table()
            QMessageBox.information(self, "Delete User", f"User '{username}' has been deleted.")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a user to delete.")

    def refresh_table(self):
        """Refrescar la tabla después de cambios."""
        self.user_table.setRowCount(len(self.user_data))
        self.populate_table()


class SystemInfoWindow(QWidget):
    def __init__(self, parent=None):
        super(SystemInfoWindow, self).__init__(parent)

        self.setWindowTitle("System Information")
        self.setStyleSheet("background-color: #3B4252; color: white;")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()

        title = QLabel("System Information")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")

        # Mostrar información del sistema
        system_info = QLabel(f"""
        <b>Operating System:</b> {platform.system()} {platform.release()}<br>
        <b>Machine:</b> {platform.machine()}<br>
        <b>Processor:</b> {platform.processor()}<br>
        <b>Total RAM:</b> {round(psutil.virtual_memory().total / (1024**3), 2)} GB<br>
        <b>Disk Space:</b> {round(psutil.disk_usage('/').total / (1024**3), 2)} GB<br>
        """)
        system_info.setStyleSheet("font-size: 12px;")
        system_info.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(system_info)
        self.setLayout(layout)
