from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
import apps.adminPanel as AdminPanel
import apps.userPanel as UserPanel
import subprocess
import sys

class AppMenu(QFrame):
    def __init__(self, parent=None, user_id=None):
        super().__init__(parent)

        if not user_id:
            raise ValueError("El 'user_id' es obligatorio para inicializar AppMenu.")

        self.user_id = user_id
        self._text_editor = None  # Referencia al editor de texto
        self._game = None  # Referencia al juego

        # Configuración del menú
        self.setFixedSize(300, 500)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.9); border-radius: 10px; padding: 10px;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.app_buttons_layout = QVBoxLayout()

        # Botones de aplicación
        self.add_app_button("Calculator", "data/icons/calc.png", parent.open_calculator)
        self.add_app_button("Task Manager", "data/icons/task.png", parent.show_task_manager)
        self.add_app_button("My Documents", "data/icons/docs.png", parent.open_docs)
        self.add_app_button("Recycle Bin", "data/icons/trash.png", parent.open_recycle_bin)
        self.add_app_button("Panel", "data/icons/pc.png", parent.open_panel)
        self.add_app_button("Music Player", "data/icons/music.png", self.open_music_player)
        self.add_app_button("Editor Text", "data/icons/text.png", self.open_text_editor)
        self.add_app_button("Weather Map", "data/icons/weather.png", parent.open_weather_map)
        self.add_app_button("Browser", "data/icons/browser.png", self.open_browser)
        self.add_app_button("Game", "data/icons/game.png", self.open_game)

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
            
            # Si no existe el editor de texto, crearlo
            if self._text_editor is None:
                self._text_editor = TextEditor(user_id=self.user_id)
                self._text_editor.destroyed.connect(self._on_text_editor_closed)
            
            # Mostrar siempre el editor de texto
            if not self._text_editor.isVisible():
                self._text_editor.show()
        except ImportError as ie:
            print(f"Error al importar TextEditor: {ie}")
        except Exception as e:
            print(f"Error al abrir el editor de texto: {e}")

    def _on_text_editor_closed(self):
        """Limpiar la referencia del editor de texto cuando se cierra."""
        self._text_editor = None

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

    def open_game(self):
        """Abrir el juego."""
        try:
            from apps.game import Game  # Importar la clase Game

            # Si no existe el juego, crearlo
            if self._game is None:
                self._game = Game()  # No se pasa user_id porque no es necesario
        
            # Mostrar siempre el juego
            if not self._game.isVisible():
                self._game.show()
        except ImportError as ie:
            print(f"Error al importar Game: {ie}")
        except Exception as e:
            print(f"Error al abrir el juego: {e}")
            
        def open_panel(self):
            """Abrir el panel de usuario o panel de administrador basado en el rol."""
            if self.role == "Administrator":
                # Mostrar el panel de administrador
                self.panel = AdminPanel(self)
            else:
                # Mostrar el panel de usuario normal
                self.panel = UserPanel(self.username, self.role, self.image_path, self)
            self.panel.show()

