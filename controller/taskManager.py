from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
import psutil  # Asegúrate de tener instalado el paquete psutil

class TaskManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Manager")
        self.setGeometry(300, 300, 400, 300)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Active Processes")
        self.layout.addWidget(self.label)

        # Lista para mostrar los procesos
        self.process_list = QListWidget(self)
        self.layout.addWidget(self.process_list)

        # Actualizar la lista de procesos al iniciar
        self.update_process_list()

    def update_process_list(self):
        """Actualizar la lista de procesos en el Task Manager."""
        self.process_list.clear()  # Limpiar la lista antes de actualizar
        processes = psutil.process_iter(['pid', 'name'])
        for process in processes:
            try:
                self.process_list.addItem(f"{process.info['pid']} - {process.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
