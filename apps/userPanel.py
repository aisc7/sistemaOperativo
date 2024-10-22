from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt
import os

class UserPanel(QWidget):
    def __init__(self, username, role, image_path, parent=None):
        super(UserPanel, self).__init__(parent)
        self.username = username
        self.role = role
        self.image_path = image_path
        
        # Configuración de la ventana
        self.setWindowTitle(f"{self.username} - User Panel")
        self.setStyleSheet("background-color: #2E3440; color: white;")
        self.setFixedSize(500, 400)
        
        # Layout principal
        self.main_layout = QVBoxLayout()
        
        # Imagen del usuario (redondeada)
        self.user_image_label = QLabel()
        self.load_user_image()
        
        # Etiqueta de nombre y rol
        self.username_label = QLabel(f"Username: {self.username}")
        self.username_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.role_label = QLabel(f"Role: {self.role.capitalize()}")
        self.role_label.setStyleSheet("font-size: 14px;")
        
        # Botón de cerrar sesión
        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet(self.get_button_style())
        self.logout_button.clicked.connect(self.logout)
        
        # Agregar elementos al layout principal
        self.main_layout.addWidget(self.user_image_label)
        self.main_layout.addWidget(self.username_label)
        self.main_layout.addWidget(self.role_label)
        
        # Opciones personalizadas según el rol
        if self.role == "admin":
            self.add_admin_controls()
        else:
            self.add_user_controls()
        
        # Botón de cerrar sesión
        self.main_layout.addWidget(self.logout_button)
        
        self.setLayout(self.main_layout)
    
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
    
    def load_user_image(self):
        """Cargar y mostrar la imagen del usuario."""
        if os.path.exists(self.image_path):
            pixmap = QPixmap(self.image_path)
            rounded_pixmap = self.get_round_pixmap(pixmap, 150)
            self.user_image_label.setPixmap(rounded_pixmap)
            self.user_image_label.setFixedSize(150, 150)
        else:
            print(f"Imagen no encontrada en la ruta: {self.image_path}")
    
    def add_admin_controls(self):
        """Agregar botones especiales para administradores."""
        self.admin_button = QPushButton("Open Admin Panel")
        self.admin_button.setStyleSheet(self.get_button_style())
        self.admin_button.clicked.connect(self.open_admin_panel)
        
        self.main_layout.addWidget(self.admin_button)
    
    def add_user_controls(self):
        """Agregar botones para usuarios regulares."""
        self.system_info_button = QPushButton("View System Info")
        self.system_info_button.setStyleSheet(self.get_button_style())
        self.system_info_button.clicked.connect(self.view_system_info)
        
        self.main_layout.addWidget(self.system_info_button)
    
    def open_admin_panel(self):
        """Abrir el panel de administración."""
        from apps.adminPanel import AdminPanel
        self.admin_window = AdminPanel(self)
        self.admin_window.show()
    
    def view_system_info(self):
        """Mostrar información del sistema."""
        QMessageBox.information(self, "System Info", "This would display system information.")
    
    def logout(self):
        """Cerrar sesión."""
        QMessageBox.information(self, "Logout", "Logging out...")
        self.close()
    
    def get_round_pixmap(self, pixmap, size):
        """Devuelve una imagen redondeada (PixMap) para mostrar como perfil."""
        rounded_pixmap = QPixmap(size, size)
        rounded_pixmap.fill(Qt.transparent)  # Hacer el fondo transparente

        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        painter.end()

        return rounded_pixmap
