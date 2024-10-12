import os
import json
import hashlib
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFormLayout, QMessageBox, QComboBox
from PySide6.QtGui import QPixmap, QPalette, QBrush, QImage, QPainter, QPainterPath
from PySide6.QtCore import Qt, QSize, QTimer, QTime, Signal as pyqtSignal
from controller.desktop import Desktop
from controller.dataBase import load_user_database, save_user_database

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 1420, 800)

        # Cargar la base de datos de usuarios
        self.user_database = self.load_user_database("data/dataBaseUser/users.json")
        
        # Inicializamos el usuario actual con el primer usuario en la base de datos o un valor por defecto
        if self.user_database:
            self.current_username = list(self.user_database.keys())[0]  # Primer usuario en la base de datos
        else:
            self.current_username = "Guest"  # Usuario por defecto si no hay usuarios

        # Verificar si la imagen de fondo existe
        path_to_background = os.path.abspath("data/background.jpg")
        if not os.path.exists(path_to_background):
            print(f"Error: Background image not found at: {path_to_background}")
        else:
            # Cargar la imagen de fondo
            background = QImage(path_to_background)
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(background.scaled(
                QSize(self.width(), self.height()),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )))
            self.setPalette(palette)

        main_layout = QHBoxLayout(self)
        main_layout.addStretch(1)

        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(15, 15, 15, 15)

        # Crear la imagen del perfil de usuario
        self.user_image_label = QLabel()
        user_image_path = os.path.abspath("data/user_image.jpeg")
        if os.path.exists(user_image_path):
            self.user_image_pixmap = QPixmap(user_image_path)
            rounded_pixmap = self.get_round_pixmap(self.user_image_pixmap, 400)
            self.user_image_label.setPixmap(rounded_pixmap)
        else:
            print(f"Error: User image not found at: {user_image_path}")

        self.user_image_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.user_image_label)

        # Botón para mostrar el nombre de usuario actual
        self.username_button = QPushButton(self.current_username)
        self.username_button.setStyleSheet("""
        QPushButton {
            background-color: rgb(183, 132, 183);
            color: white;
            font-size: 20pt;
            font-weight: bold;
            border: none;
            padding: 5px;
        }
        """)
        self.username_button.setFlat(True)
        right_layout.addWidget(self.username_button)

        # Campo de entrada para la contraseña
        form_layout = QFormLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
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
        password_label = QLabel("Password:")
        password_label.setStyleSheet("color: white; font-weight: bold;")
        form_layout.addRow(password_label, self.password_input)
        right_layout.addLayout(form_layout)

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

        # Botones para cambiar usuario e iniciar sesión
        self.change_user_button = QPushButton("Change User")
        self.login_button = QPushButton("Login")
        self.forgot_password_button = QPushButton("Forgot Password")

        self.change_user_button.setStyleSheet(button_style)
        self.login_button.setStyleSheet(button_style)
        self.forgot_password_button.setStyleSheet(button_style)

        self.change_user_button.clicked.connect(self.open_user_change_window)
        self.login_button.clicked.connect(self.handle_login)
        self.forgot_password_button.clicked.connect(self.open_password_recovery)

        right_layout.addWidget(self.change_user_button)
        right_layout.addWidget(self.login_button)
        right_layout.addWidget(self.forgot_password_button)

        main_layout.addWidget(right_container)

        # Reloj
        self.clock_label = QLabel()
        self.update_clock()
        self.clock_label.setStyleSheet("color: white; font-size: 14pt; font-weight: bold;")
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.clock_label, alignment=Qt.AlignTop | Qt.AlignRight)
        main_layout.addLayout(top_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

    def load_user_database(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading user database: {e}")
            return {}

    def get_round_pixmap(self, pixmap, size):
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
        return hashlib.sha256(password.encode()).hexdigest()

    def handle_login(self):
        user_database, first_user = self.user_database, self.current_username

        if first_user:
            username = first_user
            password = self.password_input.text()
            if username in user_database:
                hashed_password = user_database[username]['password']
                if self.hash_password(password) == hashed_password:
                    QMessageBox.information(self, "Success", f"Welcome, {username}!")
                    self.open_desktop()
                else:
                    QMessageBox.warning(self, "Error", "Incorrect password.")
            else:
                QMessageBox.warning(self, "Error", "Username does not exist.")
        else:
            QMessageBox.warning(self, "Error", "No users found. Please create a user.")

    def open_password_recovery(self):
        self.password_recovery_window = PasswordRecoveryWindow()
        self.password_recovery_window.show()

    def open_user_change_window(self):
        self.user_change_window = UserChangeWindow()
        self.user_change_window.user_changed.connect(self.update_current_user)
        self.user_change_window.show()

    def update_current_user(self, username):
        self.current_username = username
        self.username_button.setText(username)
        self.password_input.clear()
        self.load_user_image(username)
        QMessageBox.information(self, "User Changed", f"Current user changed to: {username}")

    def open_desktop(self):
        self.desktop_window = Desktop()
        self.desktop_window.show()
        self.close()

    def update_clock(self):
        current_time = QTime.currentTime()
        self.clock_label.setText(current_time.toString("hh:mm:ss"))


class PasswordRecoveryWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent  # Referencia al LoginWindow o cualquier ventana principal

        self.setWindowTitle("Password Recovery")
        self.setGeometry(400, 200, 400, 200)

        layout = QVBoxLayout(self)

        # Formulario para restablecer la contraseña
        self.reset_password_form = self.create_reset_password_form()
        layout.addLayout(self.reset_password_form)

        self.setLayout(layout)

    def create_reset_password_form(self):
        """Crea el layout para el formulario de restablecimiento de contraseña."""
        form_layout = QFormLayout()

        # ComboBox para seleccionar usuario
        self.user_selection_combo = QComboBox()
        self.update_user_selection_combo()
        form_layout.addRow(QLabel("Select User:"), self.user_selection_combo)

        # Entrada para nueva contraseña
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(QLabel("New Password:"), self.new_password_input)

        # Botón para restablecer la contraseña
        self.reset_password_button = QPushButton("Reset Password")
        self.reset_password_button.setStyleSheet(self.get_button_style())
        self.reset_password_button.clicked.connect(self.handle_reset_password)
        form_layout.addRow(self.reset_password_button)

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

    def handle_reset_password(self):
        """Lógica para restablecer la contraseña de un usuario existente."""
        selected_user = self.user_selection_combo.currentText()
        new_password = self.new_password_input.text().strip()

        if not selected_user:
            QMessageBox.warning(self, "Error", "Please select a user to reset the password.")
            return

        if not new_password:
            QMessageBox.warning(self, "Error", "Please enter a new password.")
            return

        # Cargar base de datos de usuarios
        user_database = load_user_database()

        if not user_database:
            QMessageBox.warning(self, "Error", "User database could not be loaded.")
            return

        if selected_user in user_database:
            # Verificar si el usuario tiene una estructura válida (debe ser un diccionario)
            if isinstance(user_database[selected_user], dict):
                hashed_password = self.hash_password(new_password)
                user_database[selected_user]["password"] = hashed_password
                save_user_database(user_database)
                QMessageBox.information(self, "Success", f"Password for '{selected_user}' has been reset.")
                self.close()
            else:
                QMessageBox.warning(self, "Error", f"User '{selected_user}' data is corrupted.")
        else:
            QMessageBox.warning(self, "Error", "User not found.")

    def update_user_selection_combo(self):
        """Actualiza el ComboBox con los usuarios existentes de la base de datos."""
        self.user_selection_combo.clear()  # Limpiamos el combo box
        user_database = load_user_database()

        if user_database:
            for username in user_database.keys():
                self.user_selection_combo.addItem(username)
        else:
            QMessageBox.warning(self, "Error", "No users found in the database.")

    def hash_password(self, password):
        """Hash the password using SHA-256 (or another secure method)."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    
class PasswordRecoveryWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent  # Referencia al LoginWindow o cualquier ventana principal

        self.setWindowTitle("Password Recovery")
        self.setGeometry(400, 200, 400, 200)

        layout = QVBoxLayout(self)

        # Formulario para restablecer la contraseña
        self.reset_password_form = self.create_reset_password_form()
        layout.addLayout(self.reset_password_form)

        self.setLayout(layout)

    def create_reset_password_form(self):
        """Crea el layout para el formulario de restablecimiento de contraseña."""
        form_layout = QFormLayout()

        # ComboBox para seleccionar usuario
        self.user_selection_combo = QComboBox()
        self.update_user_selection_combo()
        form_layout.addRow(QLabel("Select User:"), self.user_selection_combo)

        # Entrada para nueva contraseña
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(QLabel("New Password:"), self.new_password_input)

        # Botón para restablecer la contraseña
        self.reset_password_button = QPushButton("Reset Password")
        self.reset_password_button.setStyleSheet(self.get_button_style())
        self.reset_password_button.clicked.connect(self.handle_reset_password)
        form_layout.addRow(self.reset_password_button)

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

    def handle_reset_password(self):
        """Lógica para restablecer la contraseña de un usuario existente."""
        selected_user = self.user_selection_combo.currentText()
        new_password = self.new_password_input.text().strip()

        if not selected_user:
            QMessageBox.warning(self, "Error", "Please select a user to reset the password.")
            return

        if not new_password:
            QMessageBox.warning(self, "Error", "Please enter a new password.")
            return

        # Cargar base de datos de usuarios
        user_database = load_user_database()

        if not user_database:
            QMessageBox.warning(self, "Error", "User database could not be loaded.")
            return

        if selected_user in user_database:
            # Verificar si el usuario tiene una estructura válida (debe ser un diccionario)
            if isinstance(user_database[selected_user], dict):
                hashed_password = self.hash_password(new_password)
                user_database[selected_user]["password"] = hashed_password
                save_user_database(user_database)
                QMessageBox.information(self, "Success", f"Password for '{selected_user}' has been reset.")
                self.close()
            else:
                QMessageBox.warning(self, "Error", f"User '{selected_user}' data is corrupted.")
        else:
            QMessageBox.warning(self, "Error", "User not found.")

    def update_user_selection_combo(self):
        """Actualiza el ComboBox con los usuarios existentes de la base de datos."""
        self.user_selection_combo.clear()  # Limpiamos el combo box
        user_database = load_user_database()

        if user_database:
            for username in user_database.keys():
                self.user_selection_combo.addItem(username)
        else:
            QMessageBox.warning(self, "Error", "No users found in the database.")

    def hash_password(self, password):
        """Hash the password using SHA-256 (or another secure method)."""
        return hashlib.sha256(password.encode()).hexdigest()


class UserChangeWindow(QWidget):
    user_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Change User")
        self.setGeometry(400, 200, 400, 300)

        layout = QVBoxLayout(self)

        self.create_user_button = QPushButton("Create User")
        self.create_user_button.setStyleSheet(self.get_button_style())
        self.create_user_button.clicked.connect(self.show_create_user_fields)
        layout.addWidget(self.create_user_button)

        self.select_user_button = QPushButton("Select Existing User")
        self.select_user_button.setStyleSheet(self.get_button_style())
        self.select_user_button.clicked.connect(self.show_select_user)
        layout.addWidget(self.select_user_button)

        layout.setAlignment(Qt.AlignCenter)

        self.create_user_form_container = QWidget()
        self.create_user_form = self.create_user_form_layout()
        self.create_user_form_container.setLayout(self.create_user_form)
        layout.addWidget(self.create_user_form_container)
        self.create_user_form_container.setVisible(False)

        self.select_user_container = QWidget()
        self.select_user_layout = QVBoxLayout(self.select_user_container)
        self.user_selection_combo = QComboBox()
        self.update_user_selection_combo()
        self.select_user_layout.addWidget(self.user_selection_combo)

        self.confirm_user_button = QPushButton("Confirm Selection")
        self.confirm_user_button.setStyleSheet(self.get_button_style())
        self.confirm_user_button.clicked.connect(self.handle_select_user)
        self.select_user_layout.addWidget(self.confirm_user_button)
        layout.addWidget(self.select_user_container)
        self.select_user_container.setVisible(False)

        self.setLayout(layout)

    def get_button_style(self):
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

    def create_user_form_layout(self):
        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)

        self.confirm_create_user_button = QPushButton("Create User")
        self.confirm_create_user_button.setStyleSheet(self.get_button_style())
        self.confirm_create_user_button.clicked.connect(self.handle_create_user)
        form_layout.addWidget(self.confirm_create_user_button)

        return form_layout

    def update_user_selection_combo(self):
        user_database, _ = self.load_user_database()
        self.user_selection_combo.clear()
        self.user_selection_combo.addItems(user_database.keys())

    def show_create_user_fields(self):
        self.create_user_form_container.setVisible(True)
        self.select_user_container.setVisible(False)

    def show_select_user(self):
        self.create_user_form_container.setVisible(False)
        self.select_user_container.setVisible(True)

    def handle_create_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Both username and password are required.")
            return

        user_database, first_user = self.load_user_database()
        if username in user_database:
            QMessageBox.warning(self, "Error", "User already exists.")
        else:
            hashed_password = self.hash_password(password)
            user_database[username] = {"password": hashed_password}
            self.save_user_database(user_database)
            QMessageBox.information(self, "Success", f"User '{username}' created successfully.")
            self.user_changed.emit(username)
            self.close()

    def handle_select_user(self):
        selected_user = self.user_selection_combo.currentText()
        user_database, _ = self.load_user_database()

        if selected_user in user_database:
            QMessageBox.information(self, "Success", f"User '{selected_user}' selected.")
            self.user_changed.emit(selected_user)
            self.close()
        else:
            QMessageBox.warning(self, "Error", "User not found.")

    def load_user_database(self):
        try:
            with open("data/dataBaseUser/users.json", "r") as file:
                return json.load(file), None
        except FileNotFoundError:
            return {}, None

    def save_user_database(self, user_database):
        try:
            with open("data/dataBaseUser/users.json", "w") as file:
                json.dump(user_database, file)
        except Exception as e:
            print(f"Error saving user database: {e}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
