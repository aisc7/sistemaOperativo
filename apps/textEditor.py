import os
from PySide6.QtWidgets import QMainWindow, QTextEdit, QFileDialog, QToolBar, QMessageBox
from PySide6.QtGui import QIcon, QAction

class TextEditor(QMainWindow):
    def __init__(self, docs_path=None):
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 800, 600)

        # Crear el área de texto
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Crear una barra de herramientas
        self.toolbar = QToolBar("File Actions", self)
        self.addToolBar(self.toolbar)

        # Ruta opcional para guardar archivos
        self.docs_path = docs_path

        # Crear acciones con iconos para abrir y guardar
        open_action = QAction(QIcon.fromTheme("document-open"), "Open", self)
        open_action.triggered.connect(self.open_file)

        save_action = QAction(QIcon.fromTheme("document-save"), "Save", self)
        save_action.triggered.connect(self.save_file)

        # Añadir acciones a la barra de herramientas
        self.toolbar.addAction(open_action)
        self.toolbar.addAction(save_action)

    def open_file(self):
        """Abrir un archivo de texto y cargarlo en el editor."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    self.text_edit.setPlainText(file.read())
            except Exception as e:
                self.show_error_message(f"Error al abrir el archivo: {e}")

    def save_file(self):
        """Guardar el archivo en la carpeta 'My Docs'."""
        options = QFileDialog.Options()

        # Usa `docs_path` como la ruta predeterminada, si está disponible
        if self.docs_path:
            initial_path = os.path.join(self.docs_path, "untitled.txt")
        else:
            initial_path = "untitled.txt"  # Nombre por defecto si no hay ruta

        # Abre el diálogo de guardar archivo
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", initial_path, "Text Files (*.txt);;All Files (*)", options=options)
        
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(self.text_edit.toPlainText())
            except Exception as e:
                self.show_error_message(f"Error al guardar el archivo: {e}")

    def show_error_message(self, message):
        """Muestra un mensaje de error en caso de problemas con archivos."""
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.exec_()
