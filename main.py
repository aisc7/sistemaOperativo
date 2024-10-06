import sys 
import os
from PySide6.QtWidgets import QApplication
from controller.login import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
