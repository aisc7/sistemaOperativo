import sys
import math
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QApplication
from PySide6.QtCore import Qt

class Calculator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configuración de la ventana
        self.setWindowTitle("Scientific Calculator")
        self.setGeometry(300, 300, 400, 500)
        self.setStyleSheet("background-color: #2B2B2B; border-radius: 10px;")
        self.setWindowFlags(Qt.Window)

        layout = QVBoxLayout(self)

        # Pantalla de la calculadora
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 24px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; background-color: #FFFFFF;")
        layout.addWidget(self.display)

        # Botones de la calculadora
        grid = QGridLayout()
        buttons = [
            ('C', 0, 0), ('(', 0, 1), (')', 0, 2), ('%', 0, 3), ('/', 0, 4),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3), ('√', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3), ('^', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3), ('ln', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('sin', 4, 3), ('cos', 4, 4),
            ('tan', 5, 0), ('exp', 5, 1), ('π', 5, 2), ('e', 5, 3)
        ]

        for btn_text, x, y in buttons:
            button = QPushButton(btn_text)
            button.setFixedSize(60, 60)
            if btn_text == 'C':
                button.setStyleSheet("font-size: 20px; background-color: red; color: white; border: none; border-radius: 5px;")
            else:
                button.setStyleSheet("font-size: 20px; background-color: #3C3D37; color: white; border: none; border-radius: 5px;")
            button.clicked.connect(self.on_click)
            grid.addWidget(button, x, y)

        layout.addLayout(grid)

        # Botón de cierre
        close_button = QPushButton("Close")
        close_button.setFixedSize(60, 40)
        close_button.setStyleSheet("font-size: 16px; background-color: #FF5733; color: white; border: none; border-radius: 5px;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

    def on_click(self):
        button = self.sender().text()

        try:
            if button == '=':
                expression = self.display.text().replace('√', 'math.sqrt').replace('^', '**').replace('ln', 'math.log')
                expression = expression.replace('π', str(math.pi)).replace('e', str(math.e))
                expression = expression.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan')
                result = str(eval(expression))
                self.display.setText(result)
            elif button == 'C':
                self.display.clear()
            elif button in ('sin', 'cos', 'tan', 'ln', '√', 'exp'):
                self.display.setText(self.display.text() + f"{button}(")
            elif button == 'π':
                self.display.setText(self.display.text() + str(math.pi))
            elif button == 'e':
                self.display.setText(self.display.text() + str(math.e))
            else:
                self.display.setText(self.display.text() + button)
        except Exception:
            self.display.setText("Error")
