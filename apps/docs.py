import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem,
                               QMessageBox, QInputDialog)
from PySide6.QtGui import QIcon

class Docs(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = str(user_id)  # Asegúrate de que el ID sea una cadena
        self.setWindowTitle(f"Documents for User ID: {self.user_id}")
        self.setGeometry(200, 200, 600, 400)

        # Ruta base para guardar los documentos del usuario
        self.base_docs_path = os.path.join(os.getcwd(), 'data', 'docs', self.user_id)
        os.makedirs(self.base_docs_path, exist_ok=True)  # Crear el directorio del usuario si no existe

        # Inicializa la variable docs_path aquí
        self.docs_path = self.base_docs_path

        # Mantener un historial de carpetas para navegación
        self.history = [self.docs_path]
        self.history_index = 0

        # Inicializa la interfaz
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        nav_layout = QHBoxLayout()

        # Navegación
        self.back_button = QPushButton("←")
        self.forward_button = QPushButton("→")
        self.back_button.setEnabled(False)
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)

        main_layout.addLayout(nav_layout)

        # Explorador de archivos
        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(self.open_item)
        self.refresh_file_list()  # Llama aquí después de inicializar docs_path
        main_layout.addWidget(self.file_list)

        # Botones para crear y eliminar
        button_layout = QHBoxLayout()
        self.folder_button = QPushButton("Create Folder")
        self.file_button = QPushButton("Create File")
        self.delete_button = QPushButton("Delete Item")

        button_layout.addWidget(self.folder_button)
        button_layout.addWidget(self.file_button)
        button_layout.addWidget(self.delete_button)

        main_layout.addLayout(button_layout)

        # Conectar botones
        self.folder_button.clicked.connect(self.create_folder)
        self.file_button.clicked.connect(self.create_file)
        self.delete_button.clicked.connect(self.delete_item)
        self.back_button.clicked.connect(self.go_back)
        self.forward_button.clicked.connect(self.go_forward)

        self.setLayout(main_layout)

    def refresh_file_list(self):
        """Actualizar la lista de archivos y carpetas."""
        self.file_list.clear()

        folder_icon = QIcon("data/icons/folder.png")
        file_icon = QIcon("data/icons/file.png")

        # Listar elementos en la ruta de documentos del usuario
        try:
            for item in os.listdir(self.docs_path):
                item_path = os.path.join(self.docs_path, item)
                list_item = QListWidgetItem(item)

                if os.path.isdir(item_path):
                    list_item.setIcon(folder_icon)
                else:
                    list_item.setIcon(file_icon)

                self.file_list.addItem(list_item)
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "The documents folder could not be found.")

    def open_item(self, item):
        """Abrir el archivo o carpeta seleccionado."""
        item_path = os.path.join(self.docs_path, item.text())
        if os.path.isdir(item_path):
            self.docs_path = item_path
            self.history.append(self.docs_path)
            self.history_index += 1
            self.refresh_file_list()
            self.back_button.setEnabled(self.history_index > 0)
            self.forward_button.setEnabled(False)

    def go_back(self):
        """Navegar hacia atrás en el historial."""
        if self.history_index > 0:
            self.history_index -= 1
            self.docs_path = self.history[self.history_index]
            self.refresh_file_list()
            self.back_button.setEnabled(self.history_index > 0)
            self.forward_button.setEnabled(self.history_index < len(self.history) - 1)

    def go_forward(self):
        """Navegar hacia adelante en el historial."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.docs_path = self.history[self.history_index]
            self.refresh_file_list()
            self.back_button.setEnabled(self.history_index > 0)
            self.forward_button.setEnabled(self.history_index < len(self.history) - 1)

    def create_folder(self):
        """Crear una carpeta."""
        folder_name, ok = QInputDialog.getText(self, 'Create Folder', 'Enter folder name:')
        if ok and folder_name:
            folder_path = os.path.join(self.docs_path, folder_name)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                self.refresh_file_list()
            else:
                QMessageBox.warning(self, "Error", f"Folder '{folder_name}' already exists!")

    def create_file(self):
        """Crear un archivo con contenido."""
        file_name, ok = QInputDialog.getText(self, 'Create File', 'Enter file name:')
        if ok and file_name:
            file_path = os.path.join(self.docs_path, file_name)
            if not os.path.exists(file_path):
                file_content, ok = QInputDialog.getMultiLineText(self, 'File Content', 'Enter file content:')
                if ok:
                    with open(file_path, 'w') as file:
                        file.write(file_content)
                    self.refresh_file_list()
            else:
                QMessageBox.warning(self, "Error", f"File '{file_name}' already exists!")

    def delete_item(self):
        """Eliminar el archivo o carpeta seleccionada."""
        current_item = self.file_list.currentItem()
        if current_item:
            item_path = os.path.join(self.docs_path, current_item.text())
            if QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete '{current_item.text()}'?",
                                     QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                if os.path.isdir(item_path):
                    try:
                        os.rmdir(item_path)  # Eliminar carpeta (debe estar vacía)
                    except OSError:
                        QMessageBox.warning(self, "Error", f"Folder '{current_item.text()}' is not empty!")
                        return
                else:
                    os.remove(item_path)  # Eliminar archivo
                self.refresh_file_list()
        else:
            QMessageBox.warning(self, "Error", "No item selected for deletion!")

    def is_valid_directory(self, path):
        """Verificar si la ruta pertenece al directorio del usuario."""
        return path.startswith(self.base_docs_path)

    def closeEvent(self, event):
        """Cerrar correctamente la ventana."""
        self.deleteLater()  # Asegurarse de que la ventana se elimine correctamente
        event.accept()  # Aceptar el evento de cierre
