from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout
class Calculator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculator")
        self.setGeometry(300, 300, 300, 400)

        layout = QVBoxLayout(self)

        # Display
        self.display = QLineEdit()
        layout.addWidget(self.display)

        # Buttons grid
        grid = QGridLayout()
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
        ]

        for btn_text, x, y in buttons:
            button = QPushButton(btn_text)
            button.clicked.connect(self.on_click)
            grid.addWidget(button, x, y)

        layout.addLayout(grid)

    def on_click(self):
        button = self.sender().text()

        if button == '=':
            try:
                expression = self.display.text()
                result = str(eval(expression))
                self.display.setText(result)
            except Exception as e:
                self.display.setText("Error")
        else:
            self.display.setText(self.display.text() + button)
