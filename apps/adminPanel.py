from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

class AdminPanel(QWidget):
    def __init__(self, parent=None):
        super(AdminPanel, self).__init__(parent)
        
        self.setWindowTitle("Admin Panel")
        self.setStyleSheet("background-color: #3B4252; color: white;")
        self.setFixedSize(400, 300)
        
        self.layout = QVBoxLayout()
        
        # Título
        self.title_label = QLabel("Administration")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        # Botones de administración
        self.manage_users_button = QPushButton("Manage Users")
        self.manage_users_button.setStyleSheet(self.get_button_style())
        self.manage_users_button.clicked.connect(self.manage_users)
        
        self.view_logs_button = QPushButton("View System Logs")
        self.view_logs_button.setStyleSheet(self.get_button_style())
        self.view_logs_button.clicked.connect(self.view_system_logs)
        
        # Agregar elementos al layout
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.manage_users_button)
        self.layout.addWidget(self.view_logs_button)
        
        self.setLayout(self.layout)
    
    def get_button_style(self):
        """Devuelve el estilo del botón."""
        return """
            QPushButton {
                background-color: #4C566A;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """
    
    def manage_users(self):
        """Abrir la interfaz de gestión de usuarios."""
        QMessageBox.information(self, "Manage Users", "This would open user management interface.")
    
    def view_system_logs(self):
        """Mostrar los logs del sistema."""
        QMessageBox.information(self, "View Logs", "This would display system logs.")
