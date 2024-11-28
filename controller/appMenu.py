from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
import subprocess
import sys


class AppMenu(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 500)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.9); border-radius: 10px; padding: 10px;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.app_buttons_layout = QVBoxLayout()

        # Agregar botones para aplicaciones
        self.add_app_button("Calculator", "data/icons/calc.png", parent.open_calculator)
        self.add_app_button("Task Manager", "data/icons/task.png", parent.show_task_manager)
        self.add_app_button("My Documents", "data/icons/docs.png", parent.open_docs)
        self.add_app_button("Recycle Bin", "data/icons/trash.png", parent.open_recycle_bin)
        self.add_app_button("User Panel", "data/icons/pc.png", parent.open_user_panel)
        self.add_app_button("Music Player", "data/icons/music.png", self.open_music_player)
        self.add_app_button("Editor Text", "data/icons/text.png", self.open_text_editor)
        self.add_app_button("Weather", "data/icons/weather.png", parent.open_weather_map)
        self.add_app_button("Browser", "data/icons/browser.png", self.open_browser)  

        self.layout.addLayout(self.app_buttons_layout)

        # Botón de cierre
        close_button_layout = QHBoxLayout()
        close_button_layout.addStretch()
        close_button = QPushButton("X")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("color: white; background-color: red; border: none; border-radius: 15px;")
        close_button.clicked.connect(self.close_menu)
        close_button_layout.addWidget(close_button)
        self.layout.addLayout(close_button_layout)

    def add_app_button(self, name, icon_path, action=None):
        """Añadir un botón de aplicación al menú."""
        app_button = QPushButton()
        app_button.setIcon(QIcon(icon_path))
        app_button.setIconSize(QSize(32, 32))
        app_button.setText(name)
        app_button.setStyleSheet("color: white; text-align: left; padding: 10px; background-color: rgba(0, 0, 0, 0); border: none;")
        if action:
            app_button.clicked.connect(action)
        self.app_buttons_layout.addWidget(app_button)

    def close_menu(self):
        """Cerrar el menú de aplicaciones."""
        self.setVisible(False)

    def open_music_player(self):
        """Abrir un reproductor de música dependiendo del sistema operativo."""
        try:
            if sys.platform == "win32":
                subprocess.Popen([r"C:\Program Files\Windows Media Player\wmplayer.exe"], shell=True)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "/Applications/Music.app"])
            elif sys.platform == "linux":
                subprocess.Popen(["/snap/bin/spotify"])
            else:
                print("Sistema operativo no soportado.")
        except Exception as e:
            print(f"Error al abrir el reproductor de música: {e}")

    def open_text_editor(self):
        """Abrir un editor de texto."""
        try:
            from apps.textEditor import TextEditor  # Importar aquí para evitar dependencias circulares
            text_editor = TextEditor()  
            text_editor.show()
        except Exception as e:
            print(f"Error al abrir el editor de texto: {e}")

    def open_browser(self):
        """Abrir el navegador web predeterminado."""
        try:
            if sys.platform == "win32":
                subprocess.run(["start", "http://www.google.com"], shell=True)
            elif sys.platform == "darwin":
                subprocess.run(["open", "http://www.google.com"])
            elif sys.platform == "linux":
                subprocess.run(["xdg-open", "http://www.google.com"])
            else:
                print("Sistema operativo no soportado.")
        except Exception as e:
            print(f"Error al abrir el navegador: {e}")
