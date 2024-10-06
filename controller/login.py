import sys
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFormLayout, QMessageBox
from PySide6.QtGui import QPixmap, QPalette, QBrush, QImage, QPainter, QPainterPath
from PySide6.QtCore import Qt, QSize, QTimer, QTime
from controller.desktop import Desktop 

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 1420, 800)  # Set the window size
        
        # Get the absolute path to the background image
        path_to_background = os.path.abspath("data/background.jpg")
        
        # Check if the background image exists
        if not os.path.exists(path_to_background):
            print(f"Error: Background image not found at: {path_to_background}")
        else:
            # Load the background image
            background = QImage(path_to_background)
            
            # Create a palette and set the background image
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(background.scaled(
                QSize(self.width(), self.height()),  # Scale the image to window size
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,  # Keep the aspect ratio
                Qt.TransformationMode.SmoothTransformation  # Use smooth scaling
            )))
            self.setPalette(palette)  # Apply the palette to the window
        
        # Create the main layout (horizontal)
        main_layout = QHBoxLayout(self)
        
        # Add stretch space to the left to push elements to the right
        main_layout.addStretch(1)
        
        # Create a container for the elements on the right side
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(15, 15, 15, 15)  # Add margins to the layout
        
        # Create the user profile image
        self.user_image_label = QLabel()
        user_image_path = os.path.abspath("data/user_image.jpeg")
        if os.path.exists(user_image_path):
            # Load and scale the user profile image, then make it round
            self.user_image_pixmap = QPixmap(user_image_path)
            rounded_pixmap = self.get_round_pixmap(self.user_image_pixmap, 400)  # Size 400x400
            self.user_image_label.setPixmap(rounded_pixmap)
        else:
            print(f"Error: User image not found at: {user_image_path}")
        
        self.user_image_label.setAlignment(Qt.AlignCenter)  # Center the image
        right_layout.addWidget(self.user_image_label)
        
        # Create a QPushButton for the username
        username_button = QPushButton("Isabella")
        username_button.setStyleSheet("""
        QPushButton {
            background-color:rgb(183, 132, 183);
            color: white;
            font-size: 20pt;
            font-weight: bold;
            border: none;
            padding: 5px;
        }
        """)
        username_button.setFlat(True)  # Make the button flat so it looks more like a label
        
        # Add username button to the right layout
        right_layout.addWidget(username_button)
        
        # Create a form for entering password
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)  # Align labels to the right
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)  # Allow fields to grow
        
        # Password input field
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Set password field to hide text
        
        # Style for QLineEdit inputs
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
        
        # Style for labels
        label_style = "color: white; font-weight: bold;"
        password_label = QLabel("Password:")
        password_label.setStyleSheet(label_style)
        
        # Add password field to the form layout
        form_layout.addRow(password_label, self.password_input)
        
        right_layout.addLayout(form_layout)  # Add the form layout to the right layout
        
        # Create buttons with styles
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
        
        # Create Change User and Login buttons
        self.change_user_button = QPushButton("Change User")
        self.login_button = QPushButton("Login")
        
        # Apply the button styles
        self.change_user_button.setStyleSheet(button_style)
        self.login_button.setStyleSheet(button_style)
        
        self.login_button.clicked.connect(self.handle_login)  # Connect the login button to the login handler
        
        # Add buttons to the right layout
        right_layout.addWidget(self.change_user_button)
        right_layout.addWidget(self.login_button)
        
        # Add the right container (with all elements) to the main layout
        main_layout.addWidget(right_container)
        
        # Create the clock label
        self.clock_label = QLabel()
        self.update_clock()
        self.clock_label.setStyleSheet("color: white; font-size: 14pt; font-weight: bold;")  # Style of the clock
        
        # Add clock label to the top right of the window
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.clock_label, alignment=Qt.AlignTop | Qt.AlignRight)
        main_layout.addLayout(top_layout)
        
        # Timer to update the clock every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  # Update every second
        
        # Ensure the widget updates the background when the window is resized
        self.setAttribute(Qt.WA_StyledBackground, True)
    
    def get_round_pixmap(self, pixmap, size):
        rounded_pixmap = QPixmap(size, size)
        rounded_pixmap.fill(Qt.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, size, size, pixmap.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        painter.end()
        return rounded_pixmap
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        path_to_background = os.path.abspath("data/background.jpg")
        if os.path.exists(path_to_background):
            background = QImage(path_to_background)
            palette = self.palette()
            palette.setBrush(QPalette.Window, QBrush(background.scaled(
                QSize(self.width(), self.height()),  # Resize the background image to match the window
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,  # Keep the aspect ratio
                Qt.TransformationMode.SmoothTransformation  # Use smooth scaling
            )))
            self.setPalette(palette)
    
    def handle_login(self):
        password = self.password_input.text()
        # Example login validation (you should replace this with real validation)
        if password:
            # Close the login window
            self.close()
            # Open the desktop window
            self.desktop = Desktop()
            self.desktop.show()
        else:
            QMessageBox.warning(self, "Login Error", "Please enter password.")
    
    def update_clock(self):
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.clock_label.setText(current_time)
