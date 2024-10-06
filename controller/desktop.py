from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedLayout, QPushButton, QLabel
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, QTimer
from controller.appMenu import AppMenu
from controller.taskBar import TaskBar
from controller.calculator import Calculator
from controller.taskManager import TaskManager

class Desktop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop Simulation")

        # Mostrar la ventana en pantalla completa
        self.showFullScreen()

        # Configurar el widget central y el layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Usar QVBoxLayout para organizar los widgets verticalmente
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Crear la etiqueta para el fondo de escritorio
        self.desktop_background = QLabel(self)
        self.set_background_image("data/background.jpg")  # Cambia a la ruta de tu imagen
        main_layout.addWidget(self.desktop_background, stretch=1)  # Añadir el fondo, ocupando el espacio principal

        # Crear el área de escritorio (sobre el fondo) y añadir iconos
        desktop_area = QWidget(self.desktop_background)  # Añadir sobre el fondo
        desktop_layout = QVBoxLayout(desktop_area)
        desktop_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        desktop_layout.setContentsMargins(20, 20, 20, 20)
        self.add_desktop_icon(desktop_layout, "My Computer", "data/icons/pc.png")
        self.add_desktop_icon(desktop_layout, "Recycle Bin", "data/icons/trash.png")
        self.add_desktop_icon(desktop_layout, "My Documents", "data/icons/docs.png")

        # La barra de tareas se añade directamente en el layout principal
        self.taskbar = TaskBar(self)
        main_layout.addWidget(self.taskbar, stretch=0)  # Barra de tareas fija al fondo

        # Crear menú de aplicaciones (inicialmente oculto)
        self.app_menu = AppMenu(self)
        self.app_menu.setVisible(False)  # Aseguramos que esté oculto al inicio

        # Añadir como un widget flotante
        self.app_menu.setParent(self)
        self.app_menu.raise_()  # Asegura que está encima de otros widgets

        # Crear administrador de tareas (inicialmente oculto)
        self.task_manager = TaskManager(self)
        self.task_manager.hide()

        # Crear calculadora (inicialmente oculta)
        self.calculator = Calculator(self)
        self.calculator.hide()

        # Temporizador para actualizar el reloj cada segundo
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  # Actualizar cada segundo

    def set_background_image(self, image_path):
        """Establecer la imagen de fondo del área de escritorio."""
        pixmap = QPixmap(image_path)
        self.desktop_background.setPixmap(pixmap)
        self.desktop_background.setScaledContents(True)

    def toggle_app_menu(self):
        """Muestra u oculta el menú de aplicaciones."""
        self.app_menu.setVisible(not self.app_menu.isVisible())
        if self.app_menu.isVisible():
            # Posicionar el menú sobre la barra de tareas
            self.app_menu.move(10, self.height() - self.app_menu.height() - self.taskbar.height())
            self.app_menu.raise_()  # Asegura que se vea sobre la barra de tareas

    def show_task_manager(self):
        """Mostrar el administrador de tareas."""
        if not self.task_manager.isVisible():
            self.task_manager.update_process_list()
            self.task_manager.show()

    def show_calculator(self):
        """Mostrar la calculadora."""
        if not self.calculator.isVisible():
            self.calculator.show()

    def update_clock(self):
        """Actualizar el reloj en la barra de tareas."""
        pass

    def add_desktop_icon(self, layout, name, icon_path):
        """Agregar un icono al escritorio."""
        icon_button = QPushButton()
        icon_button.setIcon(QIcon(icon_path))
        icon_button.setIconSize(QSize(64, 64))
        icon_button.setText(name)
        icon_button.setStyleSheet("text-align: left; padding: 10px; border: none;")
        layout.addWidget(icon_button)
