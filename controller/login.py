import os
import json
import hashlib
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFormLayout, QMessageBox, QComboBox
from PySide6.QtGui import QPixmap, QPalette, QBrush, QImage, QPainter, QPainterPath
from PySide6.QtCore import Qt, QSize, QTimer, QTime
from controller.desktop import Desktop
from controller.dataBase import load_user_database, save_user_database
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 1420, 800)  # Establecer el tamaño de la ventana

        # Cargar la base de datos de usuarios desde un archivo JSON
        self.user_database = self.load_user_database("data/dataBaseUser/user.json")

        # Obtener la ruta absoluta de la imagen de fondo
        path_to_background = os.path.abspath("data/background.jpg")

        # Verificar si la imagen de fondo existe
        if not os.path.exists(path_to_background):
            print(f"Error: Background image not found at: {path_to_background}")
        else:
            # Cargar la imagen de fondo
            background = QImage(path_to_background)

            # Crear una paleta y establecer la imagen de fondo
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(background.scaled(
                QSize(self.width(), self.height()),  # Escalar la imagen al tamaño de la ventana
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,  # Mantener la relación de aspecto
                Qt.TransformationMode.SmoothTransformation  # Usar escalado suave
            )))
            self.setPalette(palette)  # Aplicar la paleta a la ventana

        # Crear el diseño principal (horizontal)
        main_layout = QHBoxLayout(self)

        # Añadir espacio de estiramiento a la izquierda para empujar elementos a la derecha
        main_layout.addStretch(1)

        # Crear un contenedor para los elementos del lado derecho
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(15, 15, 15, 15)  # Añadir márgenes al diseño

        # Crear la imagen del perfil de usuario
        self.user_image_label = QLabel()
        user_image_path = os.path.abspath("data/user_image.jpeg")
        if os.path.exists(user_image_path):
            # Cargar y escalar la imagen de perfil del usuario
            self.user_image_pixmap = QPixmap(user_image_path)
            rounded_pixmap = self.get_round_pixmap(self.user_image_pixmap, 400)  # Tamaño 400x400
            self.user_image_label.setPixmap(rounded_pixmap)
        else:
            print(f"Error: User image not found at: {user_image_path}")

        self.user_image_label.setAlignment(Qt.AlignCenter)  # Centrar la imagen
        right_layout.addWidget(self.user_image_label)

        # Crear un QPushButton para el nombre de usuario
        username_button = QPushButton("Isabella")
        username_button.setStyleSheet("""
        QPushButton {
            background-color: rgb(183, 132, 183);
            color: white;
            font-size: 20pt;
            font-weight: bold;
            border: none;
            padding: 5px;
        }
        """)
        username_button.setFlat(True)  # Hacer que el botón sea plano para que parezca más un etiqueta

        # Añadir el botón de nombre de usuario al diseño derecho
        right_layout.addWidget(username_button)

        # Crear un formulario para ingresar la contraseña
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)  # Alinear etiquetas a la derecha
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)  # Permitir que los campos crezcan

        # Campo de entrada para la contraseña
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Establecer campo de contraseña para ocultar texto

        # Estilo para entradas QLineEdit
        input_style = """
        QLineEdit {
            background-color: rgba(255, 255, 255, 200);
            border: 1px solid white;
            border-radius: 5px;
            padding: 5px;
            color: black;
        }
        """
        self.password_input.setStyleSheet(input_style)

        # Estilo para etiquetas
        label_style = "color: white; font-weight: bold;"
        password_label = QLabel("Password:")
        password_label.setStyleSheet(label_style)

        # Añadir campo de contraseña al diseño del formulario
        form_layout.addRow(password_label, self.password_input)

        right_layout.addLayout(form_layout)  # Añadir el diseño del formulario al diseño derecho

        # Crear botones con estilos
        button_style = """
        QPushButton {
            background-color: rgb(140, 48, 97);
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: rgb(82, 34, 88);
        }
        """

        # Crear botones para Cambiar Usuario, Iniciar Sesión y Olvidé la Contraseña
        self.change_user_button = QPushButton("Change User")
        self.login_button = QPushButton("Login")
        self.forgot_password_button = QPushButton("Forgot Password")  # Nuevo botón

        # Aplicar estilos a los botones
        self.change_user_button.setStyleSheet(button_style)
        self.login_button.setStyleSheet(button_style)
        self.forgot_password_button.setStyleSheet(button_style)  # Estilo para olvidar la contraseña

        # Conectar clics de botones a los manejadores correspondientes
        self.change_user_button.clicked.connect(self.open_user_change_window)  # Conectar para cambiar de usuario
        self.login_button.clicked.connect(self.handle_login)  # Conectar el botón de inicio de sesión al manejador
        self.forgot_password_button.clicked.connect(self.open_password_recovery)  # Conectar al manejador de recuperación

        # Añadir botones al diseño derecho
        right_layout.addWidget(self.change_user_button)
        right_layout.addWidget(self.login_button)
        right_layout.addWidget(self.forgot_password_button)  # Añadir al diseño

        # Añadir el contenedor derecho (con todos los elementos) al diseño principal
        main_layout.addWidget(right_container)

        # Crear la etiqueta del reloj
        self.clock_label = QLabel()
        self.update_clock()
        self.clock_label.setStyleSheet("color: white; font-size: 14pt; font-weight: bold;")  # Estilo del reloj

        # Añadir etiqueta de reloj a la parte superior derecha de la ventana
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.clock_label, alignment=Qt.AlignTop | Qt.AlignRight)
        main_layout.addLayout(top_layout)

        # Temporizador para actualizar el reloj cada segundo
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  # Actualizar cada segundo

        # Asegurarse de que el widget actualice el fondo al cambiar el tamaño de la ventana
        self.setAttribute(Qt.WA_StyledBackground, True)

    def load_user_database(self, file_path):
        """Cargar la base de datos de usuarios desde un archivo JSON."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)  # Cargar la base de datos desde el archivo
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading user database: {e}")
            return {}

    def get_round_pixmap(self, pixmap, size):
        """Crea un pixmap redondeado."""
        rounded_pixmap = QPixmap(size, size)
        rounded_pixmap.fill(Qt.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        painter.end()
        return rounded_pixmap

    def hash_password(self, password):
        """Cifra la contraseña usando SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def handle_login(self):
        """Maneja la lógica del inicio de sesión."""
        username = "Isabella"  # Aquí deberías obtener el nombre de usuario de un campo de entrada si lo necesitas
        password = self.password_input.text()

        hashed_password = self.hash_password(password)  # Cifrar la contraseña ingresada

        if username in self.user_database and self.user_database[username] == hashed_password:
            # Iniciar sesión exitosamente
            print("Login successful!")
            self.open_desktop()  # Aquí se debe abrir la ventana de escritorio
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password!")

    def open_password_recovery(self):
        """Abre la ventana de recuperación de contraseña."""
        self.password_recovery_window = PasswordRecoveryWindow()
        self.password_recovery_window.show()

    def open_user_change_window(self):
        """Abre la ventana para cambiar o crear un nuevo usuario."""
        self.user_change_window = UserChangeWindow()
        self.user_change_window.show()

    def open_desktop(self):
        """Abre la ventana de escritorio."""
        self.desktop_window = Desktop()  # Asegúrate de que Desktop esté importado
        self.desktop_window.show()
        self.close()  # Cerrar la ventana de inicio de sesión

    def update_clock(self):
        """Actualizar la etiqueta del reloj."""
        current_time = QTime.currentTime()
        self.clock_label.setText(current_time.toString("hh:mm:ss"))  # Formato de 24 horas

class PasswordRecoveryWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Password Recovery")
        self.setGeometry(400, 200, 300, 200)

        layout = QVBoxLayout(self)

        # Username
        self.username_input = QLineEdit()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)

        # New Password
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("New Password:"))
        layout.addWidget(self.new_password_input)

        # Confirm New Password
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Confirm New Password:"))
        layout.addWidget(self.confirm_password_input)

        # Recover Button
        self.recover_button = QPushButton("Recover Password")
        self.recover_button.clicked.connect(self.handle_recovery)
        layout.addWidget(self.recover_button)

    def handle_recovery(self):
        username = self.username_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if username in self.parent().user_database:
            if new_password == confirm_password:
                self.parent().user_database[username] = self.parent().hash_password(new_password)
                QMessageBox.information(self, "Success", "Password has been successfully changed.")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Passwords do not match.")
        else:
            QMessageBox.warning(self, "Error", "Username not found.")

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QFormLayout, QLabel, QLineEdit, QMessageBox
from PySide6.QtCore import Qt

class UserChangeWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent  # Guardamos la referencia al LoginWindow

        self.setWindowTitle("Change User")
        self.setGeometry(400, 200, 400, 300)

        layout = QVBoxLayout(self)

        # Botón para crear usuario
        self.create_user_button = QPushButton("Create User")
        self.create_user_button.setStyleSheet(self.get_button_style())
        self.create_user_button.clicked.connect(self.show_create_user_fields)
        layout.addWidget(self.create_user_button)

        # Botón para seleccionar usuario existente
        self.select_user_button = QPushButton("Select Existing User")
        self.select_user_button.setStyleSheet(self.get_button_style())
        self.select_user_button.clicked.connect(self.show_select_user)
        layout.addWidget(self.select_user_button)

        layout.setAlignment(Qt.AlignCenter)

        # Formulario para nuevo usuario (inicialmente oculto)
        self.create_user_form_container = QWidget()
        self.create_user_form = self.create_user_form_layout()
        self.create_user_form_container.setLayout(self.create_user_form)
        layout.addWidget(self.create_user_form_container)
        self.create_user_form_container.setVisible(False)

        # Contenedor para selección de usuario existente (inicialmente oculto)
        self.select_user_container = QWidget()
        self.select_user_layout = QVBoxLayout(self.select_user_container)

        # ComboBox para usuarios existentes
        self.user_selection_combo = QComboBox()
        self.update_user_selection_combo()
        self.select_user_layout.addWidget(self.user_selection_combo)

        # Botón para confirmar selección de usuario
        self.confirm_user_button = QPushButton("Confirm Selection")
        self.confirm_user_button.setStyleSheet(self.get_button_style())
        self.confirm_user_button.clicked.connect(self.handle_select_user)
        self.select_user_layout.addWidget(self.confirm_user_button)

        layout.addWidget(self.select_user_container)
        self.select_user_container.setVisible(False)

        self.setLayout(layout)

    def create_user_form_layout(self):
        """Crea el layout para el formulario de nuevo usuario."""
        form_layout = QFormLayout()
        
        # Entrada para ID único
        self.unique_id_input = QLineEdit()
        form_layout.addRow(QLabel("Unique ID:"), self.unique_id_input)

        # Entrada para nombre de usuario
        self.username_input = QLineEdit()
        form_layout.addRow(QLabel("Username:"), self.username_input)

        # Entrada para contraseña
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(QLabel("Password:"), self.password_input)

        # Botón para crear usuario
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet(self.get_button_style())
        self.submit_button.clicked.connect(self.handle_create_user)
        form_layout.addRow(self.submit_button)

        return form_layout

    def get_button_style(self):
        """Define el estilo de los botones."""
        return """
        QPushButton {
            background-color: rgb(140, 48, 97);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: rgb(82, 34, 88);
        }
        """

    def show_create_user_fields(self):
        """Muestra los campos para crear un nuevo usuario."""
        self.create_user_form_container.setVisible(True)
        self.select_user_container.setVisible(False)

    def show_select_user(self):
        """Muestra las opciones para seleccionar un usuario existente."""
        self.create_user_form_container.setVisible(False)
        self.select_user_container.setVisible(True)

    def handle_create_user(self):
        """Lógica para crear un nuevo usuario."""
        unique_id = self.unique_id_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if unique_id and username and password:
            user_database = load_user_database()

            # Añadir nuevo usuario
            if username not in user_database:
                hashed_password = self.parent_widget.hash_password(password)
                user_database[username] = {
                    "id": unique_id,
                    "password": hashed_password
                }
                save_user_database(user_database)  # Guardamos la base de datos actualizada
                QMessageBox.information(self, "Success", f"User '{username}' has been created.")
                self.update_user_selection_combo()  # Actualizamos el combo box
                self.close()  # Cerramos la ventana después de crear el usuario
            else:
                QMessageBox.warning(self, "Error", "Username already exists.")
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def handle_select_user(self):
        """Lógica para seleccionar un usuario existente."""
        selected_user = self.user_selection_combo.currentText()

        # Verificar que el usuario existe en la base de datos
        user_database = load_user_database()

        if selected_user in user_database:
            QMessageBox.information(self, "Success", f"User '{selected_user}' selected.")
            self.parent_widget.update_username_button(selected_user)  # Actualizamos el nombre de usuario en el login
            self.close()
        else:
            QMessageBox.warning(self, "Error", "User not found.")

    def update_user_selection_combo(self):
        """Actualiza el ComboBox con los usuarios existentes de la base de datos."""
        self.user_selection_combo.clear()  # Limpiamos el combo box

        # Cargar la base de datos de usuarios
        user_database = load_user_database()

        if user_database:
            self.user_selection_combo.addItems(user_database.keys())  # Añadimos los usuarios
        else:
            QMessageBox.warning(self, "Error", "No users found in the database.")
