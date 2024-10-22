import os
import json
import hashlib
from apps.adminPanel import AdminPanel
from controller.desktop import Desktop
from controller.dataBase import load_user_database, save_user_database
from PySide6.QtCore import Qt, QSize, QTimer, QTime, Signal as pyqtSignal
from PySide6.QtGui import QPixmap, QPalette, QBrush, QImage, QPainter, QPainterPath
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFormLayout, QMessageBox, QComboBox
import os
import json
import hashlib

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
        self.setup_background()

        main_layout = QHBoxLayout(self)
        main_layout.addStretch(1)

        right_container = QWidget()
        self.right_layout = QVBoxLayout(right_container)  # Guardar el layout en un atributo
        self.right_layout.setContentsMargins(15, 15, 15, 15)

        # Crear la imagen del perfil de usuario
        self.user_image_label = QLabel()
        self.load_user_image(self.current_username)  # Cargar imagen del usuario
        self.user_image_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.user_image_label)

        # Botón para mostrar el nombre de usuario actual
        self.username_button = QPushButton(self.current_username)
        self.username_button.setStyleSheet(self.get_button_style())
        self.username_button.setFlat(True)
        self.right_layout.addWidget(self.username_button)

        # Campo de entrada para la contraseña
        form_layout = QFormLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.get_input_style())
        password_label = QLabel("Password:")
        password_label.setStyleSheet("color: white; font-weight: bold;")
        form_layout.addRow(password_label, self.password_input)
        self.right_layout.addLayout(form_layout)

        # Botones para cambiar usuario e iniciar sesión
        self.setup_buttons()

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

    def setup_background(self):
        """Configura la imagen de fondo."""
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

    def get_input_style(self):
        """Devuelve el estilo para los campos de entrada."""
        return """
        QLineEdit {
            background-color: rgba(255, 255, 255, 200);
            border: 1px solid white;
            border-radius: 5px;
            padding: 5px;
            color: black;
        }
        """

    def get_button_style(self):
        """Devuelve el estilo para los botones."""
        return """
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

    def setup_buttons(self):
        """Configura los botones de la ventana de inicio de sesión."""
        button_style = self.get_button_style()

        self.change_user_button = QPushButton("Change User")
        self.login_button = QPushButton("Login")
        self.forgot_password_button = QPushButton("Forgot Password")

        self.change_user_button.setStyleSheet(button_style)
        self.login_button.setStyleSheet(button_style)
        self.forgot_password_button.setStyleSheet(button_style)

        self.change_user_button.clicked.connect(self.open_user_change_window)
        self.login_button.clicked.connect(self.handle_login)
        self.forgot_password_button.clicked.connect(self.open_password_recovery)

        self.right_layout.addWidget(self.change_user_button)
        self.right_layout.addWidget(self.login_button)
        self.right_layout.addWidget(self.forgot_password_button)

    def load_user_database(self, file_path):
        """Carga la base de datos de usuarios desde un archivo JSON."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading user database: {e}")
            return {}

    def load_user_image(self, username):
        """Carga la imagen del usuario basado en el nombre de usuario."""
        image_path = f"./data/userImage/{username}.jpg"  # Ruta de la imagen del usuario
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            rounded_pixmap = self.get_round_pixmap(pixmap, 400)
            self.user_image_label.setPixmap(rounded_pixmap)  # Establecer el pixmap redondeado
        else:
            # Si no hay imagen del usuario, cargar una imagen por defecto
            default_image_path = "./data/userImage/default_user.png"
            if os.path.exists(default_image_path):
                pixmap = QPixmap(default_image_path)
                rounded_pixmap = self.get_round_pixmap(pixmap, 400)
                self.user_image_label.setPixmap(rounded_pixmap)  # Establecer el pixmap por defecto
            else:
                print("No se encontró la imagen del usuario ni la imagen por defecto.")
                self.user_image_label.clear()  # Limpiar el QLabel si no hay imagen

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
        """Devuelve el hash SHA-256 de una contraseña."""
        return hashlib.sha256(password.encode()).hexdigest()

    def handle_login(self):
        """Maneja la lógica del inicio de sesión."""
        username = self.current_username  # El usuario actual seleccionado
        password = self.password_input.text()  # Contraseña ingresada

        # Verificar si el nombre de usuario existe en la base de datos
        if username in self.user_database:
            hashed_password = self.user_database[username]['password']  # Hash de la contraseña almacenada
            user_role = self.user_database[username].get('role', 'user')  # Obtener el rol, por defecto 'user'
            user_id = self.user_database[username].get('id')  # Obtener el ID del usuario

            # Verificar la contraseña
            if self.hash_password(password) == hashed_password:
                # Abrir la ventana del escritorio y pasar el ID del usuario
                self.open_desktop(user_id)
            else:
                QMessageBox.warning(self, "Error", "Incorrect password.")
        else:
            QMessageBox.warning(self, "Error", "Username does not exist.")

    def open_desktop(self, user_id):
        """Abre la ventana del escritorio según el rol del usuario."""
        self.desktop_window = Desktop(self.current_username, user_id)  # Pasar el nombre de usuario y el ID
        self.desktop_window.show()
        self.close()

    def open_admin_panel(self):
        """Abre el panel de configuración de administrador."""
        self.admin_panel_window = AdminPanel(self)  # Crear una instancia de AdminPanel
        self.admin_panel_window.show()  # Mostrar el panel de administrad

    def open_password_recovery(self):
        """Abre la ventana de recuperación de contraseña."""
        self.password_recovery_window = PasswordRecoveryWindow()
        self.password_recovery_window.show()

    def open_user_change_window(self):
        """Abre la ventana para cambiar de usuario."""
        self.user_change_window = UserChangeWindow()
        self.user_change_window.user_changed.connect(self.update_current_user)
        self.user_change_window.show()

    def update_current_user(self, username):
        """Actualiza el usuario actual al cambiar de usuario."""
        self.current_username = username
        self.username_button.setText(username)
        self.password_input.clear()
        self.load_user_image(username)  # Cargar la imagen del nuevo usuario
        QMessageBox.information(self, "User Changed", f"Current user changed to: {username}")

    def update_clock(self):
        """Actualiza el reloj en la interfaz."""
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
            
    def load_user_image(self, username):
        """Carga la imagen del usuario basado en el nombre de usuario."""
        image_path = f"./data/useImages/{username}.jpg"  
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.user_image_label.setPixmap(pixmap)
        else:
            # Si no hay imagen, puedes mostrar una imagen por defecto
            default_image_path = "./data/userImage/default_user.png"
            if os.path.exists(default_image_path):
                pixmap = QPixmap(default_image_path)
                self.user_image_label.setPixmap(pixmap)
            else:
                print("No se encontró la imagen del usuario ni la imagen por defecto.")


    def hash_password(self, password):
        """Hash the password using SHA-256 (or another secure method)."""
        return hashlib.sha256(password.encode()).hexdigest()
    

class PasswordRecoveryWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent  # Referencia a la ventana principal (LoginWindow u otra)

        self.setWindowTitle("Password Recovery")
        self.setGeometry(400, 200, 400, 250)

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

        # Entrada para el ID del usuario
        self.user_id_input = QLineEdit()
        form_layout.addRow(QLabel("Enter User ID:"), self.user_id_input)

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
        entered_user_id = self.user_id_input.text().strip()  # El ID ingresado por el usuario
        new_password = self.new_password_input.text().strip()

        if not selected_user:
            QMessageBox.warning(self, "Error", "Please select a user to reset the password.")
            return

        if not entered_user_id:
            QMessageBox.warning(self, "Error", "Please enter the user ID.")
            return

        if not new_password:
            QMessageBox.warning(self, "Error", "Please enter a new password.")
            return

        # Cargar base de datos de usuarios
        user_database = self.load_user_database()

        if not user_database:
            QMessageBox.warning(self, "Error", "User database could not be loaded.")
            return

        if selected_user in user_database:
            stored_user_id = user_database[selected_user].get("id")  # Obtener el ID del usuario

            if str(stored_user_id) != entered_user_id:
                QMessageBox.warning(self, "Error", "The entered user ID is incorrect.")
                return

            # Si el ID es correcto, procedemos con el cambio de contraseña
            hashed_password = self.hash_password(new_password)
            user_database[selected_user]["password"] = hashed_password
            self.save_user_database(user_database)
            QMessageBox.information(self, "Success", f"Password for '{selected_user}' has been reset.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "User not found.")

    def update_user_selection_combo(self):
        """Actualiza el ComboBox con los usuarios existentes de la base de datos."""
        self.user_selection_combo.clear()  # Limpiamos el combo box
        user_database = self.load_user_database()  # Cargar base de datos de usuarios

        if user_database:
            for username in user_database.keys():
                self.user_selection_combo.addItem(username)
        else:
            QMessageBox.warning(self, "Error", "No users found in the database.")

    def load_user_database(self):
        """Carga la base de datos de usuarios desde el archivo JSON."""
        try:
            with open("data/dataBaseUser/users.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}  # Retornar un diccionario vacío si no se encuentra el archivo
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Error", "User database is corrupted.")
            return {}

    def save_user_database(self, user_database):
        """Guarda la base de datos de usuarios en el archivo JSON."""
        try:
            with open("data/dataBaseUser/users.json", "w") as file:
                json.dump(user_database, file, indent=4)
        except Exception as e:
            print(f"Error saving user database: {e}")

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

        # Create user form
        self.create_user_form_container = QWidget()
        self.create_user_form = self.create_user_form_layout()
        self.create_user_form_container.setLayout(self.create_user_form)
        layout.addWidget(self.create_user_form_container)
        self.create_user_form_container.setVisible(False)

        # Select user form
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
        self.user_id_input = QLineEdit()  # Campo para ingresar el ID del usuario

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("User ID:", self.user_id_input)  # Añadir el campo para ID

        self.confirm_create_user_button = QPushButton("Create User")
        self.confirm_create_user_button.setStyleSheet(self.get_button_style())
        self.confirm_create_user_button.clicked.connect(self.handle_create_user)
        form_layout.addWidget(self.confirm_create_user_button)

        return form_layout

    def update_user_selection_combo(self):
        user_database = self.load_user_database()
        self.user_selection_combo.clear()
        self.user_selection_combo.addItems(user_database.keys())

    def show_create_user_fields(self):
        self.create_user_form_container.setVisible(True)
        self.select_user_container.setVisible(False)

    def show_select_user(self):
        self.create_user_form_container.setVisible(False)
        self.select_user_container.setVisible(True)

    def handle_create_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        user_id = self.user_id_input.text().strip()

        if not username or not password or not user_id:
            QMessageBox.warning(self, "Error", "Username, password, and user ID are required.")
            return

        user_database = self.load_user_database()

        if username in user_database:
            QMessageBox.warning(self, "Error", "User already exists.")
        elif any(user["id"] == user_id for user in user_database.values()):
            QMessageBox.warning(self, "Error", "User ID already exists. Please choose a different ID.")
        else:
            # Hash the password
            hashed_password = self.hash_password(password)

            # Create new user entry
            user_database[username] = {
                "id": user_id,
                "password": hashed_password,
                "role": "admin" if len(user_database) == 0 else "user"
            }

            self.save_user_database(user_database)
            QMessageBox.information(self, "Success", f"User '{username}' created successfully.")
            self.user_changed.emit(username)
            self.close()

    def handle_select_user(self):
        selected_user = self.user_selection_combo.currentText()
        user_database = self.load_user_database()

        if selected_user in user_database:
            QMessageBox.information(self, "Success", f"User '{selected_user}' selected.")
            self.user_changed.emit(selected_user)
            self.close()
        else:
            QMessageBox.warning(self, "Error", "User not found.")

    def load_user_database(self):
        """Carga la base de datos de usuarios desde el archivo JSON."""
        try:
            with open("data/dataBaseUser/users.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}  # Retorna un diccionario vacío si el archivo no existe

    def save_user_database(self, user_database):
        """Guarda la base de datos de usuarios en el archivo JSON."""
        try:
            with open("data/dataBaseUser/users.json", "w") as file:
                json.dump(user_database, file, indent=4)
        except Exception as e:
            print(f"Error saving user database: {e}")

    def hash_password(self, password):
        """Hash de la contraseña utilizando SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def get_next_user_id(self, user_database):
        """Obtiene el próximo ID de usuario disponible (ya no se usa ya que se permite ID personalizado)."""
        existing_ids = [user["id"] for user in user_database.values()]
        return max(existing_ids, default=0) + 1