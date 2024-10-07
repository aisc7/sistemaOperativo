from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QApplication
from PySide6.QtCore import Qt
import sys

class Calculator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configuración de la ventana
        self.setWindowTitle("Calculator")
        self.setGeometry(300, 300, 300, 400)
        self.setStyleSheet("background-color: #2B2B2B; border-radius: 10px;")  # Cambiar el color de fondo

        # Asegurarse de que la ventana tenga banderas adecuadas
        self.setWindowFlags(Qt.Window)  # Asegurarse de que la ventana tenga el comportamiento estándar de Qt

        layout = QVBoxLayout(self)

        # Pantalla de la calculadora
        self.display = QLineEdit()
        self.display.setReadOnly(True)  # Solo lectura para evitar entradas directas
        self.display.setStyleSheet("font-size: 24px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; background-color: #FFFFFF;")
        layout.addWidget(self.display)

        # Botones de la calculadora
        grid = QGridLayout()
        buttons = [
            ('C', 0, 0), ('7', 0, 1), ('8', 0, 2), ('9', 0, 3), ('/', 0, 4),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
        ]

        # Aplicar estilos a los botones
        for btn_text, x, y in buttons:
            button = QPushButton(btn_text)
            button.setFixedSize(60, 60)  # Tamaño uniforme para todos los botones
            # Estilo del botón de borrado 'C' en rojo
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
        close_button.clicked.connect(self.close)  # Conectar el botón de cierre
        layout.addWidget(close_button)

    def on_click(self):
        button = self.sender().text()

        if button == '=':
            try:
                expression = self.display.text()
                result = str(eval(expression))
                self.display.setText(result)
            except Exception:
                self.display.setText("Error")
        elif button == 'C':
            self.display.clear()  # Limpiar la pantalla al presionar 'C'
        else:
            self.display.setText(self.display.text() + button)

# Si deseas ejecutar la calculadora como una aplicación independiente, usa el siguiente bloque
if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
