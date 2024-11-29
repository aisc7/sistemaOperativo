from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QBrush, QColor, QFont
import sys


class Paddle(QGraphicsRectItem):
    def __init__(self, x, y, color):
        super().__init__(0, 0, 10, 100)
        self.setBrush(QBrush(QColor(color)))
        self.setPos(x, y)
        self.direction = 1  # 1 for down, -1 for up
        self.speed = 4  # Velocidad de movimiento de la paleta

    def move_up(self):
        if self.y() > -250:
            self.setPos(self.x(), self.y() - self.speed)

    def move_down(self):
        if self.y() < 150:
            self.setPos(self.x(), self.y() + self.speed)

    def auto_move(self):
        if self.direction == 1:
            self.move_down()
            if self.y() >= 150:
                self.direction = -1
        else:
            self.move_up()
            if self.y() <= -250:
                self.direction = 1


class Ball(QGraphicsEllipseItem):
    def __init__(self):
        super().__init__(-10, -10, 20, 20)
        self.setBrush(QBrush(QColor("white")))
        self.dx = 4  # Velocidad de movimiento de la bola en x
        self.dy = 4  # Velocidad de movimiento de la bola en y

    def move(self, left_paddle, right_paddle, game):
        self.setPos(self.x() + self.dx, self.y() + self.dy)

        # Check for collision with top and bottom walls
        if self.y() <= -290 or self.y() >= 270:
            self.dy *= -1

        # Check for collision with paddles
        if self.collidesWithItem(left_paddle) or self.collidesWithItem(right_paddle):
            self.dx *= -1

        # Check for scoring
        if self.x() <= -390:
            self.setPos(0, 0)
            self.dx *= -1
            game.increment_score("right")
        elif self.x() >= 370:
            self.setPos(0, 0)
            self.dx *= -1
            game.increment_score("left")


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pong Game")
        self.setGeometry(100, 100, 800, 600)

        self.view = QGraphicsView(self)
        self.view.setGeometry(0, 0, 800, 600)
        self.view.setStyleSheet("background-color: black;")
        self.setCentralWidget(self.view)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-400, -300, 800, 600)
        self.view.setScene(self.scene)

        # Crear paletas y pelota
        self.left_paddle = Paddle(-380, 0, "blue")
        self.right_paddle = Paddle(370, 0, "red")
        self.ball = Ball()

        # Agregar elementos a la escena
        self.scene.addItem(self.left_paddle)
        self.scene.addItem(self.right_paddle)
        self.scene.addItem(self.ball)

        # Configuración del marcador
        self.score_left = 0
        self.score_right = 0

        self.score_label_left = QLabel(f"Player A: {self.score_left}")
        self.score_label_left.setStyleSheet("color: white;")
        self.score_label_left.setFont(QFont("Arial", 16))
        self.score_label_left.setGeometry(50, 20, 200, 40)
        self.scene.addWidget(self.score_label_left)

        self.score_label_right = QLabel(f"Player B: {self.score_right}")
        self.score_label_right.setStyleSheet("color: white;")
        self.score_label_right.setFont(QFont("Arial", 16))
        self.score_label_right.setGeometry(550, 20, 200, 40)
        self.scene.addWidget(self.score_label_right)

        # Configurar temporizadores
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

        self.auto_move_timer = QTimer()
        self.auto_move_timer.timeout.connect(self.auto_move_paddle)
        self.auto_move_timer.start(16)

        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.left_paddle.move_up()
        elif event.key() == Qt.Key_S:
            self.left_paddle.move_down()

    def update_game(self):
        """Actualiza la posición de la bola y verifica colisiones."""
        self.ball.move(self.left_paddle, self.right_paddle, self)

    def auto_move_paddle(self):
        """Mueve automáticamente la paleta derecha."""
        self.right_paddle.auto_move()

    def increment_score(self, player):
        """Incrementa el marcador para el jugador correspondiente."""
        if player == "left":
            self.score_left += 1
            self.score_label_left.setText(f"Player A: {self.score_left}")
        elif player == "right":
            self.score_right += 1
            self.score_label_right.setText(f"Player B: {self.score_right}")
        print(f"Player A: {self.score_left}  Player B: {self.score_right}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec())
