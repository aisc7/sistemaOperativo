from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, QTimer
import json
import os
from controller.appMenu import AppMenu
from controller.taskBar import TaskBar
from controller.taskManager import TaskManager
from apps.calculator import Calculator
from apps.docs import Docs
from apps.trash import Trash  
from apps.userPanel import UserPanel

class Desktop(QMainWindow):
    def __init__(self, username, user_id):  # Aceptar user_id como argumento
        super().__init__()
        self.setWindowTitle("Desktop Simulation")
        self.setGeometry(100, 100, 1420, 800)

        self.username = username  # Asignar el nombre de usuario recibido
        self.user_id = user_id  # Asignar el ID del usuario recibido

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.desktop_background = QLabel(self)
        self.set_background_image("data/background.jpg")
        main_layout.addWidget(self.desktop_background, stretch=1)

        desktop_area = QWidget(self.desktop_background)
        desktop_layout = QVBoxLayout(desktop_area)
        desktop_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        desktop_layout.setContentsMargins(20, 20, 20, 20)

        # Añadir iconos al escritorio
        self.add_desktop_icon(desktop_layout, "User Panel", "data/icons/pc.png")
        self.add_desktop_icon(desktop_layout, "Recycle Bin", "data/icons/trash.png")
        self.add_desktop_icon(desktop_layout, "My Documents", "data/icons/docs.png")

        self.desktop_background.setLayout(desktop_layout)

        self.taskbar = TaskBar(self)
        main_layout.addWidget(self.taskbar, stretch=0)

        self.app_menu = AppMenu(self)
        self.app_menu.setVisible(False)
        self.app_menu.setParent(self)
        self.app_menu.raise_()

        # Instanciar las ventanas de las aplicaciones
        self.task_manager = TaskManager(self)
        self.calculator = Calculator(self)
        self.docs_window = None  # Inicializar como None
        self.trash = Trash()  # Instanciar la papelera de reciclaje

        # Inicialmente, las ventanas están ocultas
        self.task_manager.hide()
        self.calculator.hide()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        # Cargar datos del usuario
        self.role, self.image_path = self.load_user_data()  # Cambia aquí, no necesitamos el ID de nuevo

    def load_user_data(self):
        """Cargar los datos del usuario desde un archivo JSON."""
        user_data_path = "data/user_data.json"  # Ruta del archivo JSON
        
        # Verificar si el archivo existe
        if os.path.exists(user_data_path):
            with open(user_data_path, "r") as f:
                data = json.load(f)
                user = data.get(self.username)  # Obtiene el usuario correspondiente
                if user:
                    return user['role'], user.get('image_path', "data/images/default.png")  # No necesitamos el ID aquí
                else:
                    return "Invitado", "data/images/default.png"
        else:
            print("Archivo de datos de usuario no encontrado.")
            return "Invitado", "data/images/default.png"  # Valores por defecto

    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.desktop_background.setPixmap(pixmap)
        self.desktop_background.setScaledContents(True)

    def toggle_app_menu(self):
        self.app_menu.setVisible(not self.app_menu.isVisible())
        if self.app_menu.isVisible():
            self.app_menu.move(10, self.height() - self.app_menu.height() - self.taskbar.height())
            self.app_menu.raise_()

    def show_task_manager(self):
        if not self.task_manager.isVisible():
            self.task_manager.update_process_list()
            self.task_manager.update_apps_in_use()
            self.task_manager.show()
            self.task_manager.raise_()

    def open_calculator(self):
        if not self.calculator.isVisible():
            self.calculator.show()
            self.calculator.raise_()
        self.task_manager.update_apps_in_use()

    def open_docs(self):
        if self.docs_window is None:  # Si no se ha creado la ventana de Docs
            self.docs_window = Docs(self.user_id)  # Pasa el ID del usuario
        if not self.docs_window.isVisible():
            self.docs_window.show()
            self.docs_window.raise_()
        self.task_manager.update_apps_in_use()

    def open_user_panel(self):
        """Crear y mostrar el panel de usuario."""
        self.user_panel = UserPanel(self.username, self.role, self.image_path, self)
        self.user_panel.show()  # Mostrar el panel de usuario

    def open_recycle_bin(self):
        """Abrir la papelera de reciclaje."""
        self.trash.show()  # Mostrar la papelera

    def update_clock(self):
        """Lógica para actualizar el reloj, si es necesario."""
        # Implementa aquí el código para actualizar el reloj

    def add_desktop_icon(self, layout, name, icon_path):
        icon_button = QPushButton()
        icon_button.setIcon(QIcon(icon_path))
        icon_button.setIconSize(QSize(64, 64))
        icon_button.setText(name)
        icon_button.setStyleSheet("text-align: left; padding: 10px; border: none;")
        
        # Conectar las acciones de abrir el panel de usuario y la papelera
        if name == "User Panel":
            icon_button.clicked.connect(self.open_user_panel)
        elif name == "Recycle Bin":
            icon_button.clicked.connect(self.open_recycle_bin)
        elif name == "My Documents":
            icon_button.clicked.connect(self.open_docs)  # Conectar la acción de abrir el explorador de documentos

        layout.addWidget(icon_button)
