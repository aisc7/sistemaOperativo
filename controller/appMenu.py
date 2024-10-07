import sys, subprocess
from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from apps.docs import Docs  # Importar la clase Docs
from apps.calculator import Calculator  # Importar la clase Calculator

class AppMenu(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 500)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.9); border-radius: 10px; padding: 10px;")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.app_buttons_layout = QVBoxLayout()

        # Agregar botones para aplicaciones
        self.add_app_button("Calculator", "data/icons/calc.png", self.open_calculator)
        self.add_app_button("Task Manager", "data/icons/task.png", parent.show_task_manager)
        self.add_app_button("My Documents", "data/icons/docs.png", self.open_docs)
        self.add_app_button("Recycle Bin", "data/icons/trash.png", self.open_recycle_bin)
        self.add_app_button("My Computer", "data/icons/pc.png", self.open_my_computer)
        self.add_app_button("Spotife", "data/icons/music.png", self.open_music_player)

        self.layout.addLayout(self.app_buttons_layout)

        close_button_layout = QHBoxLayout()
        close_button_layout.addStretch()
        close_button = QPushButton("X")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("color: white; background-color: red; border: none; border-radius: 15px;")
        close_button.clicked.connect(self.close_menu)
        close_button_layout.addWidget(close_button)
        self.layout.addLayout(close_button_layout)

        self.docs_window = None

    def add_app_button(self, name, icon_path, action=None):
        app_button = QPushButton()
        app_button.setIcon(QIcon(icon_path))
        app_button.setIconSize(QSize(32, 32))
        app_button.setText(name)
        app_button.setStyleSheet("color: white; text-align: left; padding: 10px; background-color: rgba(0, 0, 0, 0); border: none;")
        if action:
            app_button.clicked.connect(action)
        self.app_buttons_layout.addWidget(app_button)

    def close_menu(self):
        self.setVisible(False)

    def open_docs(self):
        if not self.docs_window:
            self.docs_window = Docs()
        self.docs_window.show()

    def open_calculator(self):
        """Abrir la ventana de la calculadora."""
        self.calculator = Calculator(self)  # Crea una instancia de Calculator
        self.calculator.show()  # Muestra la ventana de la calculadora

    def open_recycle_bin(self):
        print("Open Recycle Bin")

    def open_my_computer(self):
        print("Open My Computer")

    def open_music_player(self):
        try:
            if sys.platform == "win32":
                subprocess.Popen([r"C:\Program Files\Windows Media Player\wmplayer.exe"], shell=True)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "/Applications/Music.app"])
            elif sys.platform == "linux":
                subprocess.Popen(["/snap/bin/spotify"])
            else:
                print("Unsupported Operating System")
        except Exception as e:
            print(f"Error al abrir el reproductor de música: {e}")
