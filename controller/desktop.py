from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, QTimer
from controller.appMenu import AppMenu
from controller.taskBar import TaskBar
from controller.taskManager import TaskManager
from apps.calculator import Calculator

class Desktop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop Simulation")
        self.setGeometry(100, 100, 1420, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.desktop_background = QLabel(self)
        self.set_background_image("data/background.jpg")  # Cambia la ruta de tu imagen
        main_layout.addWidget(self.desktop_background, stretch=1)

        desktop_area = QWidget(self.desktop_background)
        desktop_layout = QVBoxLayout(desktop_area)
        desktop_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        desktop_layout.setContentsMargins(20, 20, 20, 20)
        self.add_desktop_icon(desktop_layout, "My Computer", "data/icons/pc.png")
        self.add_desktop_icon(desktop_layout, "Recycle Bin", "data/icons/trash.png")
        self.add_desktop_icon(desktop_layout, "My Documents", "data/icons/docs.png")

        self.taskbar = TaskBar(self)
        main_layout.addWidget(self.taskbar, stretch=0)

        self.app_menu = AppMenu(self)
        self.app_menu.setVisible(False)
        self.app_menu.setParent(self)
        self.app_menu.raise_()

        self.task_manager = TaskManager(self)
        self.task_manager.hide()

        self.calculator = Calculator(self)
        self.calculator.hide()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

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
            self.task_manager.show()

    def update_clock(self):
        pass  # Implementar lógica para actualizar el reloj

    def add_desktop_icon(self, layout, name, icon_path):
        icon_button = QPushButton()
        icon_button.setIcon(QIcon(icon_path))
        icon_button.setIconSize(QSize(64, 64))
        icon_button.setText(name)
        icon_button.setStyleSheet("text-align: left; padding: 10px; border: none;")
        layout.addWidget(icon_button)

