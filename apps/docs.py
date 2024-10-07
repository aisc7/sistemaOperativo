import os
from PySide6.QtWidgets import ( QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QListWidget,QListWidgetItem,QMessageBox, QInputDialog,
)
from PySide6.QtGui import QIcon

class Docs(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Documents")
        self.setGeometry(200, 200, 600, 400)

        # Ruta base para guardar los documentos
        self.base_docs_path = os.path.join(os.getcwd(), 'data', 'docs')
        self.docs_path = self.base_docs_path
        os.makedirs(self.base_docs_path, exist_ok=True)  # Crear el directorio docs si no existe

        # Mantener un historial de carpetas para navegación
        self.history = [self.docs_path]
        self.history_index = 0

        # Layout principal
        main_layout = QVBoxLayout(self)

        # Flechas de navegación
        nav_layout = QHBoxLayout()
        self.back_button = QPushButton("←")
        self.forward_button = QPushButton("→")
        self.back_button.setEnabled(False)  # Deshabilitar el botón "Atrás" al inicio
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)

        main_layout.addLayout(nav_layout)

        # Explorador de archivos (list view)
        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(self.open_item)  # Conectar doble clic a la función open_item
        self.refresh_file_list()  # Cargar archivos y carpetas actuales
        main_layout.addWidget(self.file_list)

        # Botones para crear carpetas y archivos
        button_layout = QHBoxLayout()
        self.folder_button = QPushButton("Create Folder")
        self.file_button = QPushButton("Create File")
        self.delete_button = QPushButton("Delete Item")  # Botón para eliminar

        button_layout.addWidget(self.folder_button)
        button_layout.addWidget(self.file_button)
        button_layout.addWidget(self.delete_button)

        main_layout.addLayout(button_layout)

        # Conectar botones con funciones
        self.folder_button.clicked.connect(self.create_folder)
        self.file_button.clicked.connect(self.create_file)
        self.delete_button.clicked.connect(self.delete_item)  # Conectar el botón de eliminación
        self.back_button.clicked.connect(self.go_back)  # Conectar el botón de retroceso
        self.forward_button.clicked.connect(self.go_forward)  # Conectar el botón de avance

    def refresh_file_list(self):
        """Actualizar la lista de archivos y carpetas en la interfaz."""
        self.file_list.clear()  # Limpiar la lista antes de recargar

        # Íconos para archivos y carpetas
        folder_icon = QIcon("data/icons/folder.png")  # Asegúrate de que esta ruta sea correcta
        file_icon = QIcon("data/icons/file.png")      # Asegúrate de que esta ruta sea correcta

        # Recorrer los elementos en el directorio de documentos
        for item in os.listdir(self.docs_path):
            item_path = os.path.join(self.docs_path, item)
            list_item = QListWidgetItem(item)  # Crear un nuevo elemento en la lista

            if os.path.isdir(item_path):
                list_item.setIcon(folder_icon)  # Asignar ícono de carpeta si es un directorio
            else:
                list_item.setIcon(file_icon)  # Asignar ícono de archivo si es un archivo

            self.file_list.addItem(list_item)  # Añadir el elemento a la lista

    def open_item(self, item):
        """Abrir el archivo o carpeta seleccionado."""
        item_path = os.path.join(self.docs_path, item.text())
        if os.path.isdir(item_path):
            # Navegar a la carpeta seleccionada
            self.docs_path = item_path
            self.history.append(self.docs_path)  # Agregar a historial
            self.history_index += 1
            self.refresh_file_list()  # Actualizar la lista para mostrar el contenido de la nueva carpeta
            
            # Habilitar el botón "Atrás" si es posible
            self.back_button.setEnabled(self.history_index > 0)
            self.forward_button.setEnabled(False)  # Reiniciar el botón "Adelante"

    def go_back(self):
        """Navegar hacia atrás en el historial."""
        if self.history_index > 0:
            self.history_index -= 1
            self.docs_path = self.history[self.history_index]
            self.refresh_file_list()  # Actualizar la vista de la lista
            
            # Habilitar o deshabilitar botones de navegación
            self.back_button.setEnabled(self.history_index > 0)
            self.forward_button.setEnabled(self.history_index < len(self.history) - 1)

    def go_forward(self):
        """Navegar hacia adelante en el historial."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.docs_path = self.history[self.history_index]
            self.refresh_file_list()  # Actualizar la vista de la lista
            
            # Habilitar o deshabilitar botones de navegación
            self.back_button.setEnabled(self.history_index > 0)
            self.forward_button.setEnabled(self.history_index < len(self.history) - 1)

    def create_folder(self):
        """Abrir un diálogo para crear una carpeta."""
        folder_name, ok = QInputDialog.getText(self, 'Create Folder', 'Enter folder name:')
        if ok and folder_name:
            folder_path = os.path.join(self.docs_path, folder_name)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                self.refresh_file_list()  # Actualizar la vista de la lista
            else:
                QMessageBox.warning(self, "Error", f"Folder '{folder_name}' already exists!")

    def create_file(self):
        """Abrir un diálogo para crear un archivo con contenido."""
        file_name, ok = QInputDialog.getText(self, 'Create File', 'Enter file name:')
        if ok and file_name:
            file_path = os.path.join(self.docs_path, file_name)
            if not os.path.exists(file_path):
                file_content, ok = QInputDialog.getMultiLineText(self, 'File Content', 'Enter file content:')
                if ok:
                    with open(file_path, 'w') as file:
                        file.write(file_content)
                    self.refresh_file_list()  # Actualizar la vista de la lista
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
                    os.rmdir(item_path)  # Eliminar carpeta (debe estar vacía)
                else:
                    os.remove(item_path)  # Eliminar archivo
                self.refresh_file_list()  # Actualizar la lista
        else:
            QMessageBox.warning(self, "Error", "No item selected for deletion!")
