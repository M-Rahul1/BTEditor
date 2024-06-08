import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import QBrush, QColor, QPen

class Cup(QGraphicsRectItem):
    def __init__(self, x: float, y: float, width: float, height: float, color: QColor, label: str):
        super().__init__(x, y, width, height)
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.black, 2))  # Set a black pen with width 2

        self.label = QGraphicsTextItem(label, self)
        self.label.setDefaultTextColor(Qt.black)
        self.label.setPos(x, y - 20)

        self.content = QGraphicsRectItem(x, y, width, 0, self)
        self.content.setBrush(QBrush(color))
        
        self.content_level = 0

    def set_content_level(self, level: float):
        self.content_level = level
        self.content.setRect(self.rect().x(), self.rect().y() + self.rect().height() - level, self.rect().width(), level)

    def transfer_content(self, amount: float) -> float:
        new_level = max(0, self.content_level - amount)
        transferred_amount = self.content_level - new_level
        self.set_content_level(new_level)
        return transferred_amount

class SimulationScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 600, 400)
        self.big_cup = Cup(250, 50, 100, 150, QColor(255, 255, 255), "Big Cup")
        self.addItem(self.big_cup)

        self.sugar_cup = Cup(100, 250, 50, 100, QColor(255, 255, 255), "Sugar")
        self.sugar_cup.set_content_level(100)
        self.addItem(self.sugar_cup)

        self.milk_cup = Cup(250, 250, 50, 100, QColor(192, 192, 192), "Milk")
        self.milk_cup.set_content_level(100)
        self.addItem(self.milk_cup)

        self.coffee_cup = Cup(400, 250, 50, 100, QColor(139, 69, 19), "Coffee")
        self.coffee_cup.set_content_level(100)
        self.addItem(self.coffee_cup)

        self.cups = {"sugar": self.sugar_cup, "milk": self.milk_cup, "coffee": self.coffee_cup}
        self.current_action = None

    def execute_action(self, action: str):
        if action in self.cups:
            self.current_action = action
            QTimer.singleShot(50, self.transfer_step)

    def transfer_step(self):
        if self.current_action:
            cup = self.cups[self.current_action]
            amount = cup.transfer_content(5)
            self.big_cup.set_content_level(self.big_cup.content_level + amount)

            if cup.content_level > 0:
                QTimer.singleShot(50, self.transfer_step)
            else:
                self.current_action = None

class SimulationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Behavior Tree Simulation")
        self.setGeometry(100, 100, 600, 400)

        self.view = QGraphicsView()
        self.scene = SimulationScene()
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        # Simulating the behavior tree actions
        QTimer.singleShot(1000, lambda: self.scene.execute_action("sugar"))
        QTimer.singleShot(3000, lambda: self.scene.execute_action("milk"))
        QTimer.singleShot(5000, lambda: self.scene.execute_action("coffee"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimulationWindow()
    window.show()
    sys.exit(app.exec_())
