from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QIcon, QPixmap
from controller.taskManager import TaskManager
from apps.api.weatherMap import WeatherMapWindow
from controller.appMenu import AppMenu
from apps.adminPanel import AdminPanel
from controller.taskBar import TaskBar
from apps.calculator import Calculator
from apps.userPanel import UserPanel
from apps.trash import Trash
from apps.docs import Docs
import subprocess
import json
import os
import sys


class Desktop(QMainWindow):
    def __init__(self, username, user_id):
        super().__init__()
        self.setWindowTitle("Desktop Simulation")
        self.setGeometry(100, 100, 1420, 800)

        self.username = username  # Nombre de usuario recibido
        self.user_id = user_id  # ID del usuario recibido

        # Crear el widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Fondo del escritorio
        self.desktop_background = QLabel(self)
        self.set_background_image("data/background.jpg")
        main_layout.addWidget(self.desktop_background, stretch=1)

        # Área de escritorio para íconos
        desktop_area = QWidget(self.desktop_background)
        desktop_layout = QVBoxLayout(desktop_area)
        desktop_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        desktop_layout.setContentsMargins(20, 20, 20, 20)

        # Ventanas de las aplicaciones
        self.trash = Trash()  # Instanciar la papelera de reciclaje
        self.docs_window = None  # Inicializar como None
        self.weather_map_window = None  # Inicializar como None

        # Añadir iconos al escritorio
        self.add_desktop_icon(desktop_layout, "Panel", "data/icons/pc.png")
        self.add_desktop_icon(desktop_layout, "Recycle Bin", "data/icons/trash.png")
        self.add_desktop_icon(desktop_layout, "My Documents", "data/icons/docs.png")
        self.add_desktop_icon(desktop_layout, "Weather", "data/icons/weather.png")
        self.add_desktop_icon(desktop_layout, "Browser", "data/icons/browser.png")

        self.desktop_background.setLayout(desktop_layout)

        # Barra de tareas
        self.taskbar = TaskBar(self)
        main_layout.addWidget(self.taskbar, stretch=0)

        # Menú de aplicaciones
        self.app_menu = AppMenu(self, user_id=self.user_id)
        self.app_menu.setVisible(False)

        # Administrador de tareas
        self.task_manager = TaskManager(self)
        self.task_manager.hide()

        # Calculadora
        self.calculator = Calculator(self)
        self.calculator.hide()

        # Reloj
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        # Cargar datos del usuario
        self.role, self.image_path = self.load_user_data()

    def load_user_data(self):
        """Cargar los datos del usuario desde un archivo JSON."""
        user_data_path = "data/dataBaseUser/users.json"

        if os.path.exists(user_data_path):
            with open(user_data_path, "r") as f:
                data = json.load(f)
                user = data.get(self.username)  # Obtener los datos del usuario
                if user:
                    return user['role'], user.get('image_path', "data/images/default.png")
        print("Archivo de datos de usuario no encontrado o usuario no registrado.")
        return "Invitado", "data/images/default.png"

    def set_background_image(self, image_path):
        """Establecer la imagen de fondo."""
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Advertencia: No se pudo cargar el fondo desde {image_path}.")
        self.desktop_background.setPixmap(pixmap)
        self.desktop_background.setScaledContents(True)

    def toggle_app_menu(self):
        """Mostrar u ocultar el menú de aplicaciones."""
        self.app_menu.setVisible(not self.app_menu.isVisible())
        if self.app_menu.isVisible():
            self.app_menu.move(10, self.height() - self.app_menu.height() - self.taskbar.height())
            self.app_menu.raise_()

    def show_task_manager(self):
        """Mostrar el administrador de tareas."""
        if not self.task_manager.isVisible():
            self.task_manager.update_process_list()
            self.task_manager.update_apps_in_use()
            self.task_manager.show()
            self.task_manager.raise_()

    def open_calculator(self):
        """Abrir la calculadora."""
        if not self.calculator.isVisible():
            self.calculator.show()
            self.calculator.raise_()
        self.task_manager.update_apps_in_use()

    def open_docs(self):
        """Abrir documentos."""
        if self.docs_window is None:
            self.docs_window = Docs(self.user_id)  # Pasar user_id
        if not self.docs_window.isVisible():
            self.docs_window.show()
            self.docs_window.raise_()
        self.task_manager.update_apps_in_use()

    def open_panel(self):
        """Abrir el panel de usuario o administrador según el rol."""
        if self.role == "Administrator":
            self.panel = AdminPanel(self)
        else:
            self.panel = UserPanel(self.username, self.role, self.image_path, self)
        self.panel.show()

    def open_recycle_bin(self):
        """Abrir la papelera de reciclaje."""
        if self.trash:
            self.trash.show()
        else:
            print("Error: La papelera de reciclaje no está disponible.")

    def open_weather_map(self):
        """Abrir la ventana del mapa del clima."""
        try:
            if self.weather_map_window is None:
                self.weather_map_window = WeatherMapWindow()
            if not self.weather_map_window.isVisible():
                self.weather_map_window.show()
                self.weather_map_window.raise_()
        except Exception as e:
            print(f"Error al abrir el mapa del clima: {e}")

    def add_desktop_icon(self, layout, name, icon_path):
        """Añadir un ícono al escritorio."""
        icon_button = QPushButton()
        icon_button.setIcon(QIcon(icon_path))
        icon_button.setIconSize(QSize(64, 64))
        icon_button.setText(name)
        icon_button.setStyleSheet("text-align: left; padding: 10px; border: none;")

        # Conectar las acciones de los íconos
        if name == "Panel":
            icon_button.clicked.connect(self.open_panel)
        elif name == "Recycle Bin":
            icon_button.clicked.connect(self.open_recycle_bin)
        elif name == "My Documents":
            icon_button.clicked.connect(self.open_docs)
        elif name == "Weather":
            icon_button.clicked.connect(self.open_weather_map)
        elif name == "Browser":
            icon_button.clicked.connect(self.open_browser)

        layout.addWidget(icon_button)

    def update_clock(self):
        """Actualizar el reloj (implementación futura)."""
        pass

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
