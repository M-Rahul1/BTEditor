import math
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPainter, QPen, QBrush, QPixmap
from PyQt5.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QPolygonF, QGraphicsRectItem
from PyQt5.QtCore import QRectF, QPointF



class SimulationDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Simulation", parent)
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateSimulation)
        self.timer.start(16)  # approximately 60 FPS
        self.robot_pos = [500, 650]
        self.robot_carrying = None
        self.part1_pos = [100, 150]
        self.part2_pos = [100, 200]
        self.part3_pos = [100, 250]
        self.part4_pos = [100, 300]
        self.parts= ['part1', 'part2', 'part3', 'part4']

    def initUI(self):
        self.setFloating(False)
        self.simulationWidget = QWidget()
        self.setWidget(self.simulationWidget)

        layout = QVBoxLayout()
        self.simulationWidget.setLayout(layout)

        self.graphicsView = QGraphicsView()
        layout.addWidget(self.graphicsView)

        self.graphicsScene = QGraphicsScene()
        self.graphicsView.setScene(self.graphicsScene)

        self.drawStations()  # Draw initial stations and parts

    def updateSimulation(self):
        self.graphicsScene.clear()
        self.drawStations()
        self.drawRobot()
        self.drawParts()

    def drawStations(self):
        self.drawStation(100, 100, "Parts Station", Qt.red)
        self.drawStation(400, 100, "Assembly Station", Qt.green)
        self.drawStation(700, 100, "Storage Station", Qt.blue)

    def drawStation(self, x, y, label, color):
        # Create a QPixmap to draw on
        pixmap = QPixmap(150, 350)
        pixmap.fill(Qt.transparent)  # Fill with transparent background

        # Create a QPainter and set up drawing parameters
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the rectangle with color and outline
        rect = QRectF(0, 0, 150, 350)
        pen = QPen(Qt.black)
        brush = QBrush(color)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(rect)

        # Draw label inside the rectangle
        font = QFont()
        font.setPointSize(12)  # Adjust font size as needed
        painter.setFont(font)
        painter.setPen(Qt.black)
        painter.drawText(rect, Qt.AlignCenter, label)

        painter.end()  # Finish painting on the QPixmap

        # Convert the QPixmap to a QGraphicsPixmapItem and add to scene
        pixmap_item = QGraphicsPixmapItem(pixmap)
        pixmap_item.setPos(x, y)
        self.graphicsScene.addItem(pixmap_item)

    def drawParts(self):
        self.drawPart(self.part1_pos[0], self.part1_pos[1], "Part1", Qt.yellow)
        self.drawPart(self.part2_pos[0], self.part2_pos[1], "Part2", Qt.yellow)
        self.drawPart(self.part3_pos[0], self.part3_pos[1], "Part3", Qt.yellow)
        self.drawPart(self.part4_pos[0], self.part4_pos[1], "Part4", Qt.yellow)

    def drawPart(self, x, y, label, color):
        partRect = QRectF(x - 10, y - 10, 20, 20)
        rect_item = QGraphicsRectItem(partRect)
        rect_item.setPen(Qt.black)
        rect_item.setBrush(color)  # Use provided color for the part
        self.graphicsScene.addItem(rect_item)

    def drawRobot(self):
        x, y = self.robot_pos
        points = self.hexagon_points(self.robot_pos)
        self.graphicsScene.addPolygon(QPolygonF(points), QPen(Qt.black), QBrush(Qt.gray))

    def hexagon_points(self, pos):
        x, y = pos
        size = 40
        points = [
            QPointF(x + size * math.cos(math.radians(angle)), y + size * math.sin(math.radians(angle)))
            for angle in range(0, 360, 60)
        ]
        return points

    def move_part1(self, target_x, target_y):       
        while self.part1_pos != [target_x, target_y]:
            if self.part1_pos[0] < target_x:
                self.part1_pos[0] += 5
            elif self.part1_pos[0] > target_x:
                self.part1_pos[0] -= 5
            if self.part1_pos[1] < target_y:
                self.part1_pos[1] += 5
            elif self.part1_pos[1] > target_y:
                self.part1_pos[1] -= 5
    
    def move_part2(self, target_x, target_y):       
        while self.part2_pos != [target_x, target_y]:
            if self.part2_pos[0] < target_x:
                self.part2_pos[0] += 5
            elif self.part2_pos[0] > target_x:
                self.part2_pos[0] -= 5
            if self.part2_pos[1] < target_y:
                self.part2_pos[1] += 5
            elif self.part2_pos[1] > target_y:
                self.part2_pos[1] -= 5
                
    def move_part3(self, target_x, target_y):
        while self.part3_pos != [target_x, target_y]:
            if self.part3_pos[0] < target_x:
                self.part3_pos[0] += 5
            elif self.part3_pos[0] > target_x:
                self.part3_pos[0] -= 5
            if self.part3_pos[1] < target_y:
                self.part3_pos[1] += 5
            elif self.part3_pos[1] > target_y:
                self.part3_pos[1] -= 5   
                
    def move_part4(self, target_x, target_y):
        while self.part4_pos != [target_x, target_y]:
            if self.part4_pos[0] < target_x:
                self.part4_pos[0] += 5
            elif self.part4_pos[0] > target_x:
                self.part4_pos[0] -= 5
            if self.part4_pos[1] < target_y:
                self.part4_pos[1] += 5
            elif self.part4_pos[1] > target_y:
                self.part4_pos[1] -= 5             

    def move_robot(self, target_x, target_y):
        while self.robot_pos != [target_x, target_y]:
            if self.robot_pos[0] < target_x:
                self.robot_pos[0] += 5
            elif self.robot_pos[0] > target_x:
                self.robot_pos[0] -= 5

            if self.robot_pos[1] < target_y:
                self.robot_pos[1] += 5
            elif self.robot_pos[1] > target_y:
                self.robot_pos[1] -= 5

            QTimer.singleShot(10, self.updateSimulation)
            self.update()

    def execute_sequence(self):
        self.execute_action("pick_part")
        self.execute_action("place_part_in_assembly")
        self.execute_action("store_product")

    def execute_action(self, action: str):
        if action == "pick_part":
            self.move_robot(175, 275)  # Example target position
            self.pick_part()
        elif action == "place_part_in_assembly":
            self.move_robot(475, 275)  # Example target position
            self.move_part1(400, 150)
            self.move_part2(400, 200)
            self.move_part3(400, 250)
            self.move_part4(400, 300)
            
            self.place_part_in_assembly()
        elif action == "store_product":
            self.move_robot(775, 275)  # Example target position
            self.move_part1(700, 150)
            self.move_part2(700, 200)
            self.move_part3(700, 250)
            self.move_part4(700, 300)
            self.store_product()

    def pick_part(self):
        if self.parts:
            part = self.parts.pop(0)
            self.robot_carrying = part

    def place_part_in_assembly(self):
        if self.robot_carrying:
            self.robot_carrying = None

    def store_product(self):
        if self.robot_carrying:
            self.robot_carrying = None