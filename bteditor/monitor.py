import os
import json
from PyQt5.QtWidgets import QAction, QMessageBox
from nodeeditor.utils import dumpException
from PyQt5.QtCore import *


class SceneMonitor():
    """Class contains all the code for monitoring the scene"""
    def __init__(self, scene):
        """
        :param scene: Reference to the :class:`~nodeeditor.node_scene.Scene`
        :type scene: :class:`~nodeeditor.node_scene.Scene`

        :Instance Attributes:

        - **scene** - reference to the :class:`~nodeeditor.node_scene.Scene`
        """
        self.scene = scene
        self.node_list = []
        self.monitor_timer = None

    def monitor(self):
        # Monitor the flow of the graph and color the nodes
        self.node_list = self.scene.nodes[:] 
        for node in self.node_list:
            content_widget = node.grNode.content
            content_widget.setStyleSheet("background-color: #FF0000;")
        self.monitor_timer = QTimer() 
        self.monitor_timer.timeout.connect(self.colorNextNode)  
        self.monitor_timer.start(2000)  

    def colorNextNode(self):
        
        if self.node_list:
            node = self.node_list.pop(0)  
            content_widget = node.grNode.content
           
                # Check if the node's ID is "sequence"
            if node.title == "Sequence":
                if self.areChildNodesGreen(node):
                    content_widget.setStyleSheet("background-color: #00FF00;")
                else:
                    content_widget.setStyleSheet("background-color: #FF0000;")
            else:
                content_widget.setStyleSheet("background-color: #00FF00;")

        else:
            # If all nodes have been colored, stop the timer
            self.monitor_timer.stop()

    def areChildNodesGreen(self, node):
        # Recursive function to check if all child nodes are green
        for child_node in node.getChildrenNodes():
            if child_node.grNode.content.styleSheet() != "background-color: #00FF00;":
                return False
            if not self.areChildNodesGreen(child_node):
                return False
        return True            

    def getChildrenNodes(self, node):
        self.edge_list = self.scene.edges[:] 
        children_nodes = []
        sequence_nodes = []
        self.node_list = self.scene.nodes[:] 
        for node in self.node_list:
            if node.title == "Sequence":
                sequence_nodes.append(node)
                
        for edge in self.edge_list:
            if edge.start== sequence_nodes:
                children_nodes.append(edge.end)
        return children_nodes