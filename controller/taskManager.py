import psutil
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QTabWidget, QTableWidget, QTableWidgetItem)
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter

class TaskManager(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Almacenar referencia a las apps abiertas
        self.parent = parent

        # Configurar la ventana principal
        self.setWindowTitle("Administrador de Tareas")
        self.setGeometry(100, 100, 800, 600)

        # Crear las pestañas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Crear las pestañas de Rendimiento, Procesos y Apps en uso
        self.performance_tab = QWidget()
        self.processes_tab = QWidget()
        self.apps_in_use_tab = QWidget()

        # Añadir las pestañas
        self.tabs.addTab(self.performance_tab, "Rendimiento")
        self.tabs.addTab(self.processes_tab, "Procesos")
        self.tabs.addTab(self.apps_in_use_tab, "Apps en uso")

        # Configurar la pestaña de rendimiento
        self.setup_performance_tab()

        # Configurar la pestaña de procesos
        self.setup_processes_tab()

        # Configurar la pestaña de Apps en uso
        self.setup_apps_in_use_tab()

        # Crear un temporizador para actualizar los datos de rendimiento y procesos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Actualizar cada segundo

    def setup_performance_tab(self):
        layout = QVBoxLayout()

        # Etiquetas para mostrar el uso de CPU y memoria
        self.cpu_label = QLabel("CPU: ")
        self.memory_label = QLabel("Memoria: ")

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)

        # Crear un gráfico de líneas para mostrar el uso de la CPU
        self.cpu_series = QLineSeries()
        self.chart = QChart()
        self.chart.addSeries(self.cpu_series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("Uso de CPU")

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(self.chart_view)

        self.performance_tab.setLayout(layout)

    def setup_processes_tab(self):
        layout = QVBoxLayout()

        # Crear una tabla para mostrar los procesos en ejecución
        self.processes_table = QTableWidget()
        self.processes_table.setColumnCount(2)
        self.processes_table.setHorizontalHeaderLabels(["PID", "Nombre del Proceso"])

        layout.addWidget(self.processes_table)
        self.processes_tab.setLayout(layout)

    def setup_apps_in_use_tab(self):
        layout = QVBoxLayout()

        # Crear una tabla para mostrar las apps en uso
        self.apps_table = QTableWidget()
        self.apps_table.setColumnCount(1)
        self.apps_table.setHorizontalHeaderLabels(["Apps en uso"])

        layout.addWidget(self.apps_table)
        self.apps_in_use_tab.setLayout(layout)

    def update_data(self):
        """Actualizar los datos de rendimiento y la lista de procesos y apps en uso."""
        self.update_performance_data()
        self.update_process_list()
        self.update_apps_in_use()

    def update_process_list(self):
        """Actualizar la lista de procesos."""
        self.processes_table.setRowCount(0)  # Limpiar la tabla de procesos

        # Obtener la lista de procesos usando psutil
        for idx, proc in enumerate(psutil.process_iter(['pid', 'name'])):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                self.processes_table.insertRow(idx)
                self.processes_table.setItem(idx, 0, QTableWidgetItem(str(pid)))
                self.processes_table.setItem(idx, 1, QTableWidgetItem(name))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def update_performance_data(self):
        """Actualizar datos de rendimiento del sistema."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()

        # Actualizar las etiquetas de CPU y memoria
        self.cpu_label.setText(f"CPU: {cpu_percent}%")
        self.memory_label.setText(f"Memoria: {memory_info.used / (1024 ** 3):.2f} GB / {memory_info.total / (1024 ** 3):.2f} GB")

        # Añadir el uso de la CPU al gráfico
        if len(self.cpu_series.pointsVector()) > 100:  # Limitar el gráfico a 100 puntos
            self.cpu_series.removePoints(0, 1)

        self.cpu_series.append(len(self.cpu_series.pointsVector()), cpu_percent)

    def update_apps_in_use(self):
        """Actualizar la lista de aplicaciones en uso."""
        self.apps_table.setRowCount(0)  # Limpiar la tabla de apps en uso

        open_apps = []
        if self.parent.calculator.isVisible():
            open_apps.append("Calculator")
        if self.parent.docs_window and self.parent.docs_window.isVisible():
            open_apps.append("Docs")

        # Añadir más aplicaciones si se abren más
        # Aquí puedes añadir lógica para otras aplicaciones

        # Llenar la tabla con las apps abiertas
        for idx, app_name in enumerate(open_apps):
            self.apps_table.insertRow(idx)
            self.apps_table.setItem(idx, 0, QTableWidgetItem(app_name))
