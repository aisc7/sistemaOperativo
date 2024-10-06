from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class AppMenu(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 500)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.9); border-radius: 10px; padding: 10px;")

        self.layout = QVBoxLayout(self)  # Inicializa el layout y lo asigna a la instancia

    def add_app_button(self, name, icon_path, action=None):
        app_button = QPushButton()
        app_button.setIcon(QIcon(icon_path))
        app_button.setIconSize(QSize(32, 32))
        app_button.setText(name)
        app_button.setStyleSheet("color: white; text-align: left; padding: 10px; background-color: rgba(0, 0, 0, 0); border: none;")
        if action:
            app_button.clicked.connect(action)
        self.layout.addWidget(app_button)  # Usa el layout de la instancia para agregar el botón
