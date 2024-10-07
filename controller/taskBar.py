import psutil
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, QTime, QSize

class TaskBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgb(140, 48, 97); border-top: 1px solid #ccc;")
        self.setFixedHeight(50)  # Fijar una altura constante para la barra de tareas

        # Layout horizontal para la barra de tareas
        taskbar_layout = QHBoxLayout(self)
        taskbar_layout.setContentsMargins(10, 5, 10, 5)
        taskbar_layout.setSpacing(20)  # Añadir espaciado entre los elementos

        # Botón de inicio (Start Menu)
        start_button = QPushButton()
        start_button.setIcon(QIcon("data/icons/start.png"))  # Asegúrate de que la ruta del icono es correcta
        start_button.setIconSize(QSize(32, 32))
        start_button.setStyleSheet("border: none;")
        start_button.clicked.connect(parent.toggle_app_menu)  # Vincula la acción para mostrar el menú de aplicaciones
        taskbar_layout.addWidget(start_button)

        # Reloj
        self.clock_label = QLabel()
        self.update_clock()  # Inicializa el reloj
        self.clock_label.setStyleSheet("color: white; font-size: 14pt; font-weight: bold;")
        taskbar_layout.addWidget(self.clock_label)

        # Icono de batería
        self.battery_label = QLabel()
        self.update_battery_status()  # Inicializa el estado de la batería
        self.battery_label.setStyleSheet("color: white; font-size: 14pt;")
        taskbar_layout.addWidget(self.battery_label)

        # Timer para actualizar el reloj y el estado de la batería cada segundo
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)  # Actualiza el reloj
        self.timer.timeout.connect(self.update_battery_status)  # Actualiza el estado de la batería
        self.timer.start(1000)  # Ejecutar cada segundo

    def update_clock(self):
        """Actualizar la hora actual en el formato hh:mm:ss AM/PM."""
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.clock_label.setText(current_time)

    def update_battery_status(self):
        """Actualizar el estado de la batería si está disponible."""
        battery = psutil.sensors_battery()
        if battery is not None:
            percent = battery.percent
            plugged = battery.power_plugged
            if plugged:
                self.battery_label.setText(f"Battery: {percent}% (Charging)")
            else:
                self.battery_label.setText(f"Battery: {percent}%")
        else:
            # Si no se puede obtener el estado de la batería (por ejemplo, en un escritorio)
            self.battery_label.setText("Battery: N/A")