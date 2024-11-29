from PySide6.QtWidgets import QMainWindow, QDialog, QTextEdit, QToolBar, QMessageBox, QInputDialog, QFileDialog, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton
from PySide6.QtGui import QAction
import os

class TextEditor(QMainWindow):
    def __init__(self, user_id=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 800, 600)

        # Configurar la ruta de los documentos del usuario
        self.docs_path = os.path.join(os.getcwd(), 'data', 'docs', self.user_id)
        print(f"Ruta de documentos del usuario: {self.docs_path}")  # Verificación de la ruta
        os.makedirs(self.docs_path, exist_ok=True)  # Crear el directorio si no existe

        # Configurar editor de texto
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Configurar barra de herramientas
        self.toolbar = QToolBar("File Actions", self)
        self.addToolBar(self.toolbar)

        # Crear acciones
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)

        # Añadir acciones a la barra
        self.toolbar.addAction(open_action)
        self.toolbar.addAction(save_action)


    def open_file(self):
        """Abrir un archivo desde la carpeta 'My Docs'"""
        # Crear la carpeta 'My Docs' si no existe
        my_docs_path = os.path.join(self.docs_path, "My Docs")
        os.makedirs(my_docs_path, exist_ok=True)

        # Crear un cuadro de diálogo personalizado para mostrar los archivos
        dialog = QDialog(self)
        dialog.setWindowTitle("Open File")
        dialog.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout(dialog)

        # Lista de archivos
        file_list = QListWidget(dialog)
        file_list.setSelectionMode(QListWidget.SingleSelection)
        for file_name in os.listdir(my_docs_path):
            # Mostrar solo archivos
            file_path = os.path.join(my_docs_path, file_name)
            if os.path.isfile(file_path):
                file_list.addItem(file_name)

        layout.addWidget(file_list)

        # Botones de acción
        button_layout = QHBoxLayout()
        open_button = QPushButton("Open", dialog)
        cancel_button = QPushButton("Cancel", dialog)
        button_layout.addWidget(open_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        # Conectar botones
        open_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        # Mostrar el diálogo y manejar la selección
        if dialog.exec_() == QDialog.Accepted:
            selected_item = file_list.currentItem()
            if selected_item:
                selected_file = selected_item.text()
                file_path = os.path.join(my_docs_path, selected_file)

                try:
                    # Abrir archivo y cargar contenido en el editor
                    with open(file_path, 'r') as file:
                        self.text_edit.setPlainText(file.read())
                    QMessageBox.information(self, "File Opened", f"File '{selected_file}' opened successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not open file: {e}")
        else:
            QMessageBox.information(self, "Cancelled", "No file was selected.")


    def save_file(self):
        """Guardar un archivo en la carpeta 'My Docs' dentro de los documentos del usuario."""
        # Crear la carpeta 'My Docs' si no existe
        my_docs_path = os.path.join(self.docs_path, "My Docs")
        os.makedirs(my_docs_path, exist_ok=True)

        # Solicitar nombre del archivo
        file_name, ok = QInputDialog.getText(self, "Save File", "Enter file name (with extension):")
        if ok and file_name:
            # Asegurarse de que el archivo tenga una extensión
            if not os.path.splitext(file_name)[1]:
                file_name += ".txt"  # Agregar una extensión predeterminada si no se especifica

            file_path = os.path.join(my_docs_path, file_name)  # Guardar en 'My Docs'

            # Validar si el archivo ya existe
            if os.path.exists(file_path):
                overwrite = QMessageBox.question(
                    self,
                    "Overwrite File",
                    f"The file '{file_name}' already exists. Do you want to overwrite it?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if overwrite != QMessageBox.Yes:
                    return  # Salir si el usuario decide no sobrescribir

            try:
                # Guardar el archivo
                with open(file_path, 'w') as file:
                    file.write(self.text_edit.toPlainText())
                QMessageBox.information(self, "Success", f"File saved as '{file_name}' in 'My Docs'")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")
