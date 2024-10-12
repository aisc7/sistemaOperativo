from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox

class Trash(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recycle Bin")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Recycle Bin")
        self.layout.addWidget(self.label)

        self.trash_list = QListWidget()
        self.layout.addWidget(self.trash_list)

        # Botones para gestionar la papelera
        self.restore_button = QPushButton("Restore Selected")
        self.restore_button.clicked.connect(self.restore_selected)
        self.layout.addWidget(self.restore_button)

        self.empty_button = QPushButton("Empty Recycle Bin")
        self.empty_button.clicked.connect(self.empty_trash)
        self.layout.addWidget(self.empty_button)

    def add_item(self, item_name):
        """Agrega un ítem a la papelera."""
        self.trash_list.addItem(item_name)

    def restore_selected(self):
        """Restaura el ítem seleccionado de la papelera."""
        selected_items = self.trash_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No item selected.")
            return

        for item in selected_items:
            self.trash_list.takeItem(self.trash_list.row(item))  # Eliminar de la lista de la papelera
            # Aquí debes implementar la lógica para restaurar el archivo o elemento a su ubicación original

        QMessageBox.information(self, "Success", "Selected item restored.")

    def empty_trash(self):
        """Vacía la papelera."""
        self.trash_list.clear()
        QMessageBox.information(self, "Success", "Recycle Bin emptied.")
