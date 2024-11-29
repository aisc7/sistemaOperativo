import os
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem,
    QMessageBox, QInputDialog, QFileDialog
)
from PySide6.QtGui import QIcon

def load_user_data():
    """Carga los datos del archivo JSON y devuelve el diccionario de usuarios."""
    # Ruta absoluta para acceder al archivo 'user.json'
    user_json_path = '/media/isa/IsaLinux/Prog-Linux/sistemaOperativo/data/dataBaseUser/user.json'
    
    # Si prefieres usar una ruta relativa, usa esta línea en su lugar:
    # user_json_path = os.path.join(os.path.dirname(__file__), 'data', 'dataBaseUser', 'user.json')

    print(f"Intentando cargar el archivo JSON desde: {user_json_path}")
    try:
        with open(user_json_path, 'r') as f:
            users = json.load(f)
        return users
    except FileNotFoundError:
        print(f"Archivo 'user.json' no encontrado en {user_json_path}.")
        return None
    except json.JSONDecodeError:
        print("Error al leer el archivo JSON.")
        return None

def get_user_id(user_name):
    """Obtiene el id de un usuario por su nombre."""
    users = load_user_data()
    if users and user_name in users:
        return users[user_name]["id"]
    return None  # Si el usuario no se encuentra

class Docs(QWidget):
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.user_id = str(get_user_id(user_name))  # Obtener el ID del usuario
        self.setWindowTitle("My Documents")
        self.setGeometry(200, 200, 600, 400)

        # Configurar la ruta base de los documentos
        self.base_docs_path = os.path.join(os.getcwd(), 'data', 'docs', self.user_id)
        os.makedirs(self.base_docs_path, exist_ok=True)

        self.docs_path = self.base_docs_path
        self.history = [self.docs_path]
        self.history_index = 0

        self.init_ui()

    def init_ui(self):
        """Inicializar la interfaz gráfica."""
        main_layout = QVBoxLayout(self)

        # Navegación
        nav_layout = QHBoxLayout()
        self.back_button = QPushButton("←")
        self.forward_button = QPushButton("→")
        self.back_button.setEnabled(False)
        self.forward_button.setEnabled(False)
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)

        # Lista de archivos
        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(self.open_item)

        # Botones
        button_layout = QHBoxLayout()
        self.folder_button = QPushButton("Create Folder")
        self.file_button = QPushButton("Create File")
        self.delete_button = QPushButton("Delete Item")
        self.close_button = QPushButton("Close")  # Botón de cerrar
        button_layout.addWidget(self.folder_button)
        button_layout.addWidget(self.file_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.close_button)

        # Conectar botones
        self.folder_button.clicked.connect(self.create_folder)
        self.file_button.clicked.connect(self.create_file)
        self.delete_button.clicked.connect(self.delete_item)
        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)
        self.close_button.clicked.connect(self.close)  # Acción de cerrar ventana

        # Añadir al layout principal
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.file_list)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.refresh_file_list()

    def refresh_file_list(self):
        """Actualizar la lista de archivos y carpetas."""
        self.file_list.clear()
        folder_icon = QIcon("data/icons/folder.png")
        file_icon = QIcon("data/icons/file.png")
        for item in os.listdir(self.docs_path):
            item_path = os.path.join(self.docs_path, item)
            list_item = QListWidgetItem(item)
            list_item.setIcon(folder_icon if os.path.isdir(item_path) else file_icon)
            self.file_list.addItem(list_item)

    def open_item(self, item):
        """Abrir una carpeta."""
        item_path = os.path.join(self.docs_path, item.text())
        if os.path.isdir(item_path):
            self.docs_path = item_path
            self.history.append(self.docs_path)
            self.history_index += 1
            self.refresh_file_list()

    def go_back(self):
        """Navegar hacia atrás en el historial."""
        if self.history_index > 0:
            self.history_index -= 1
            self.docs_path = self.history[self.history_index]
            self.refresh_file_list()

    def go_forward(self):
        """Navegar hacia adelante en el historial."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.docs_path = self.history[self.history_index]
            self.refresh_file_list()

    def create_folder(self):
        """Crear una nueva carpeta."""
        folder_name, ok = QInputDialog.getText(self, 'Create Folder', 'Enter folder name:')
        if ok and folder_name:
            folder_path = os.path.join(self.docs_path, folder_name)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                self.refresh_file_list()
            else:
                QMessageBox.warning(self, "Error", f"Folder '{folder_name}' already exists!")

    def create_file(self):
        """Crear un nuevo archivo."""
        file_name, ok = QInputDialog.getText(self, 'Create File', 'Enter file name:')
        if ok and file_name:
            file_path = os.path.join(self.docs_path, file_name)
            if not os.path.exists(file_path):
                open(file_path, 'w').close()
                self.refresh_file_list()
            else:
                QMessageBox.warning(self, "Error", f"File '{file_name}' already exists!")

    def delete_item(self):
        """Eliminar un archivo o carpeta."""
        current_item = self.file_list.currentItem()
        if current_item:
            item_path = os.path.join(self.docs_path, current_item.text())
            if QMessageBox.question(self, "Confirm Delete", f"Delete '{current_item.text()}'?",
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                if os.path.isdir(item_path):
                    os.rmdir(item_path)
                else:
                    os.remove(item_path)
                self.refresh_file_list()

    def select_file(self):
        """Permitir al usuario seleccionar un archivo dentro de Docs."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", self.docs_path)
        return file_name

    def select_folder(self):
        """Permitir al usuario seleccionar una carpeta dentro de Docs."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", self.docs_path)
        return folder
