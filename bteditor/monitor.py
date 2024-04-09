import os
import json
from PyQt5.QtWidgets import QAction, QMessageBox
from nodeeditor.utils import dumpException
from nodeeditor.node_editor_window import NodeEditorWindow


class MonitorController:
    @staticmethod
    def Monitor():
        try:
            calculator_window = CalculatorWindow()
            calculator_window.loadNodesAndEdgesFromJson("")
            calculator_window.Monitor()
        except Exception as e:
            dumpException(e)


class CalculatorWindow(NodeEditorWindow):
    def __init__(self):
        super().__init__()

    def Monitor(self):
        for node in self.nodes:
            node.onSelected(True)

    def loadNodesAndEdgesFromJson(self, json_folder):
        example_file = os.path.join(json_folder, "example.json")
        with open(example_file, "r") as f:
            data = json.load(f)
        self.nodes = data["nodes"]
        self.edges = data["edges"]  


class MonitorAction(QAction):
    def __init__(self, parent=None):
        super().__init__("&Monitor", parent)
        self.setStatusTip("Color nodes and edges in tree structure")
        self.triggered.connect(MonitorController.Monitor)
