import os, sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import json
import py_trees as pt
import pygame
import threading
import math

from nodeeditor.utils import loadStylesheets
from nodeeditor.node_editor_window import NodeEditorWindow
from nodeeditor.node_editor_widget import NodeEditorWidget
from bteditor.sub_window import CalculatorSubWindow
from bteditor.drag_listbox import QDMDragListbox
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_graphics_edge import QDMGraphicsEdge
from nodeeditor.utils import dumpException, pp
from bteditor.conf import *
from bteditor.output_log import OutputDock
#from bteditor.simu_coffee import PygameSimulation
#from bteditor.simu_ai_car import PygameSimulation

# Enabling edge validators
from nodeeditor.node_edge import Edge
from nodeeditor.node_edge_validators import *
Edge.registerEdgeValidator(edge_validator_debug)
Edge.registerEdgeValidator(edge_cannot_connect_two_outputs_or_two_inputs)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_same_node)

# images for the dark skin
import bteditor.qss.nodeeditor_dark_resources
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

DEBUG = False

class PygameSimulation(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.parts = ["part1", "part2", "part3", "part4", "part5", "part6", "part7", "part8", "part9", "part10"]
        self.assembled_product = None
        self.storage = []
        self.current_task = None
        self.robot_pos = [500, 750]
        self.robot_carrying = None

    def run(self):
        pygame.init()
        WIDTH, HEIGHT = 1000, 800
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Assembly Robot Simulation")

        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        BLACK = (0, 0, 0)
        GREY = (192, 192, 192)

        run = True
        clock = pygame.time.Clock()

        class Station:
            def __init__(self, x, y, label, color):
                self.rect = pygame.Rect(x, y, 150, 350)
                self.label = label
                self.color = color
                self.content = []

            def draw(self, win):
                pygame.draw.rect(win, self.color, self.rect)
                font = pygame.font.SysFont(None, 24)
                text = font.render(self.label, True, BLACK)
                win.blit(text, (self.rect.x + 5, self.rect.y + 5))
                for i, part in enumerate(self.content):
                    if part == "product":
                        part_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 40, 50, 50)
                    else:
                        part_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 40 + i * 30, 20, 20)
                    pygame.draw.rect(win, BLACK, part_rect)

        parts_station = Station(100, 100, "Parts Station", RED)
        assembly_station = Station(400, 100, "Assembly Station", GREEN)
        storage_station = Station(700, 100, "Storage Station", BLUE)

        self.stations = {
            "parts_station": parts_station,
            "assembly_station": assembly_station,
            "storage_station": storage_station
        }

        self.stations["parts_station"].content = self.parts.copy()

        while run:
            if not self.running:
                pygame.quit()
                break

            clock.tick(60)
            WIN.fill(WHITE)
            pygame.draw.rect(WIN, GREY, (0, 0, WIDTH, HEIGHT))  # Draw floor

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Draw stations
            parts_station.draw(WIN)
            assembly_station.draw(WIN)
            storage_station.draw(WIN)

            # Draw robot
            pygame.draw.polygon(WIN, BLACK, self.hexagon_points(self.robot_pos))

            # Draw robot carrying part or product
            if self.robot_carrying:
                if self.robot_carrying == "product":
                    part_rect = pygame.Rect(self.robot_pos[0] - 25, self.robot_pos[1] - 25, 50, 50)
                else:
                    part_rect = pygame.Rect(self.robot_pos[0] - 10, self.robot_pos[1] - 10, 20, 20)
                pygame.draw.rect(WIN, BLACK, part_rect)

            pygame.display.update()

        pygame.quit()

    def hexagon_points(self, pos):
        x, y = pos
        size = 40
        points = [
            (x + size * math.cos(math.radians(angle)), y + size * math.sin(math.radians(angle)))
            for angle in range(0, 360, 60)
        ]
        return points

    def execute_sequence(self):
        for _ in range(len(self.parts)):
            self.execute_action("pick_part")
            self.execute_action("place_part_in_assembly")
            self.execute_action("assemble_product")
            self.execute_action("store_product")

    def move_robot(self, target_station_key):
        target_station = self.stations[target_station_key].rect
        target_pos = [target_station.x + target_station.width // 2, target_station.y + target_station.height // 2]

        while self.robot_pos != target_pos:
            time.sleep(0.01)
            if self.robot_pos[0] < target_pos[0]:
                self.robot_pos[0] += 5
            elif self.robot_pos[0] > target_pos[0]:
                self.robot_pos[0] -= 5

            if self.robot_pos[1] < target_pos[1]:
                self.robot_pos[1] += 5
            elif self.robot_pos[1] > target_pos[1]:
                self.robot_pos[1] -= 5

    def execute_action(self, action: str):
        if action == "pick_part":
            self.move_robot("parts_station")
            self.pick_part()
        elif action == "place_part_in_assembly":
            self.move_robot("assembly_station")
            self.place_part_in_assembly()
        elif action == "assemble_product":
            self.assemble_product()
        elif action == "store_product":
            self.move_robot("storage_station")
            self.store_product()

    def pick_part(self):
        if self.parts:
            part = self.parts.pop(0)
            self.robot_carrying = part
            self.stations["parts_station"].content.remove(part)

    def place_part_in_assembly(self):
        if self.robot_carrying:
            self.stations["assembly_station"].content.append(self.robot_carrying)
            
    def assemble_product(self):
        if len(self.stations["assembly_station"].content) >= 4:
            for _ in range(2):
                self.stations["assembly_station"].content.pop(0) 

    def store_product(self):
        if self.robot_carrying:
            self.stations["assembly_station"].content.pop(0)
            self.stations["storage_station"].content.append(self.robot_carrying)
        #no more action to be taken
        self.robot_carrying = None

    def start_simulation(self):
        self.running = True
        self.start()

    def stop_simulation(self):
        self.running = False
        self.join()


class CalculatorWindow(NodeEditorWindow):
    def __init__(self):
        super().__init__()
        self.status_bar = self.statusBar()
        self.timer = QTimer()
        self.bt_tree = None
        self.simulation_thread = PygameSimulation()

    def toggleSimulation(self):
        if self.simulationDock.isVisible():
            self.simulationDock.hide()
            if self.simulation_thread:
                self.simulation_thread.stop_simulation()
        else:
            self.simulationDock.show()
            self.simulation_thread = PygameSimulation()  # Create a new instance
            self.simulation_thread.start_simulation()

    def createSimulationDock(self):       
        self.simulationDock = QDockWidget("Simulation")
        self.simulationDock.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.simulationDock) 
        self.simulationDock.hide()

    def update_node_colors(self):
        for index, node in enumerate(self.node_list):
            connected_nodes = self.get_connected_nodes(node)
            if node not in connected_nodes:
                continue

            content_widget = node.grNode.content
            status = node.py_trees_object.status.value
            node_number = index + 1
            print(f'Node {node_number} ({node.op_title}) : Status {status}')
            self.status_bar.showMessage(f'Node : {node.op_title}               Status : {status}')
            if status == 'SUCCESS':
                content_widget.setStyleSheet("background-color: green;")
                if node.op_title == "Light_is_red?":
                    self.simulation_thread.execute_action("red")
                elif node.op_title == "Light_is_green?":
                    self.simulation_thread.execute_action("green")
                elif node.op_title == "Assist_patient":
                    self.simulation_thread.execute_action("attend_patient")
                elif node.op_title == "Move_to_medicine":
                    self.simulation_thread.execute_action("to_medicine")
                elif node.op_title == "Move_to_patient":
                    self.simulation_thread.execute_action("deliver_to_patient")
                    pygame.time.wait(120)
                elif node.op_title == "Add_coffee!":
                    self.simulation_thread.execute_action("coffee")
                elif node.op_title == "Add_milk!":
                    self.simulation_thread.execute_action("milk")
                elif node.op_title == "Add_sugar!":
                    self.simulation_thread.execute_action("sugar")
                    pygame.time.wait(120)
                elif node.op_title == "Power_critical_system":
                    self.simulation_thread.execute_action("power_critical_system")
                elif node.op_title == "Store_excess_energy":
                    self.simulation_thread.execute_action("store_excess_energy")
                elif node.op_title == "Power_non_critical_system":
                    self.simulation_thread.execute_action("power_non_critical_system")
                elif node.op_title == "Use_stored_energy":
                    self.simulation_thread.execute_action("use_stored_energy")
                    pygame.time.wait(120)
                elif node.op_title == "Pick_parts":
                    self.simulation_thread.execute_action("pick_part")
                elif node.op_title == "Place_parts_in_assembly":
                    self.simulation_thread.execute_action("place_part_in_assembly")
                elif node.op_title == "Assemble_product":
                    self.simulation_thread.execute_action("assemble_product")                
                elif node.op_title == "Store_product":
                    self.simulation_thread.execute_action("store_product")
                
            elif status == 'RUNNING':
                content_widget.setStyleSheet("background-color: orange;")
            elif status == 'FAILURE':
                content_widget.setStyleSheet("background-color: red;")
                if node.op_title == "No_emergency?":
                    self.simulation_thread.execute_action("needs_help") 
            else:
                content_widget.setStyleSheet("background-color: black;")
                            
    def initUI(self):
        self.name_company = 'ABB'
        self.name_product = 'NodeEditor'

        self.stylesheet_filename = os.path.join(os.path.dirname(__file__), "qss/nodeeditor.qss")
        loadStylesheets(
            os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss"),
            self.stylesheet_filename
        )

        self.empty_icon = QIcon(".")
        self.icon = QIcon(os.path.join(os.path.dirname(__file__), 'icons/abb.png'))
        self.openimg = QIcon(os.path.join(os.path.dirname(__file__), 'data/icons/folder_page.png'))
        self.saveimg = QIcon(os.path.join(os.path.dirname(__file__), 'data/icons/save.png'))
        self.undoimg = QIcon(os.path.join(os.path.dirname(__file__), 'data/icons/undo1.png'))
        self.redoimg = QIcon(os.path.join(os.path.dirname(__file__), 'data/icons/redo1.png'))
        self.buildimg = QIcon(os.path.join(os.path.dirname(__file__), 'data/icons/wrench_blue.png'))
        self.runimg = QIcon(os.path.join(os.path.dirname(__file__), 'icons/play.png'))
        self.tickimg= QIcon(os.path.join(os.path.dirname(__file__), 'data/icons/tick.png'))
        self.pauseimg= QIcon(os.path.join(os.path.dirname(__file__), 'data/icons/pause.png'))
        self.resetimg= QIcon(os.path.join(os.path.dirname(__file__), 'data/icons/reset.png'))
        self.simuimg= QIcon(os.path.join(os.path.dirname(__file__), 'data/icons/simulate.png'))
        if DEBUG:
            print("Registered nodes:")
            pp(CALC_NODES)


        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createNodesDock()
        
        self.createSimulationDock()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()

        self.setWindowTitle("BT NodeEditor")
        self.setWindowIcon(self.icon)
        
        # Creating and adding OutputDock
        self._dockOutput = OutputDock('Output', self)
        self._dockOutput.setObjectName('output')
        self._dockOutput.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._dockOutput)
        
        # Redirecting stdout to the output dock
        sys.stdout = self._dockOutput
        self._dockOutput.setStyleSheet("QTextEdit { font-size: 11pt; }")

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()
            # hacky fix for PyQt 5.14.x
            import sys
            sys.exit(0)

    def createToolBars(self):
        super().createToolBars()
        self.toolbar = self.addToolBar("Tools")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setIconSize(QSize(24, 24))
        
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        
        self.toolbar.addAction(self.actNew1)
        self.toolbar.addAction(self.actSave1)
        self.toolbar.addAction(self.undo1)
        self.toolbar.addAction(self.redo1)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)
        
        self.toolbar.addAction(self.actBuild1)
        self.toolbar.addAction(self.actRunOnce1)
        self.toolbar.addAction(self.actRun1)
        self.toolbar.addAction(self.actPause1)
        self.toolbar.addAction(self.actReset1) 
        self.toolbar.addAction(self.actSimulate)       
        
    def createActions(self):
        super().createActions()

        self.actNew1= QAction(self.openimg, "New", self, triggered=self.onFileNew)
        self.actSave1= QAction(self.saveimg, "Save", self, triggered=self.onFileSaveAs)
        self.undo1= QAction(self.undoimg, "Undo", self, triggered=self.onEditUndo)
        self.redo1= QAction(self.redoimg, "Redo", self, triggered=self.onEditRedo)
        self.actBuild1 = QAction(self.buildimg, "Build Tree", self, triggered=self.onBuild)
        self.actRunOnce1 = QAction(self.tickimg, "Tick Once", self, triggered=self.onRunOnce)
        self.actRun1 = QAction(self.runimg, "Tick Until Result", self, triggered=self.onRun)
        self.actPause1 = QAction(self.pauseimg, "Pause", self, triggered=self.onPause)
        self.actReset1 = QAction(self.resetimg, "Reset", self, triggered=self.onReset)
        self.actSimulate = QAction(self.simuimg,"Simulate", self, triggered=self.toggleSimulation)
        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)
    
    def changeColor(self, color):
        """Change color of the edge from string hex value '#00ff00'"""
        self._color = QColor(color) if type(color) == str else color
        self._pen = QPen(self._color)
        self._pen.setWidthF(3.0)

    def onFileSave(self):
        """Handle File Save operation"""
        current_nodeeditor = self.getCurrentNodeEditorWidget()
        if current_nodeeditor is not None:
            if not current_nodeeditor.isFilenameSet(): return self.onFileSaveAs()

            current_nodeeditor.fileSave()
            self.statusBar().showMessage("Successfully saved %s" % current_nodeeditor.filename, 5000)

            # support for MDI app
            if hasattr(current_nodeeditor, "setTitle"): current_nodeeditor.setTitle()
            else: self.setTitle()
            return True
        
    def get_connected_nodes(self, node):
        connected_nodes = set()
        for node in self.node_list:
            for socket in node.inputs:
                for edge in socket.edges:
                    if edge.start_socket.node != node:
                        connected_node = edge.start_socket.node
                        connected_nodes.add(connected_node)
            for socket in node.outputs:
                for edge in socket.edges:
                    if edge.end_socket.node != node:
                        connected_node = edge.end_socket.node
                        connected_nodes.add(connected_node)
        return connected_nodes
    
    def showWarningMessage(self, message):
        QMessageBox.warning(self, 'Warning', message)
    
    def onBuild(self):
        current_node_editor = self.getCurrentNodeEditorWidget()
        self.node_list = current_node_editor.scene.nodes[:]
        unconnected_nodes = []
        
        for node in self.node_list:
            connected_nodes = self.get_connected_nodes(node)
            
            if node not in connected_nodes:
                unconnected_nodes.append(node)
                continue  # Skip styling and conversion for unconnected nodes
            
            content_widget = node.grNode.content
            content_widget.setStyleSheet("background-color: lightgrey;")
        
        if unconnected_nodes:
            warning_message = "Warning: The following nodes are not connected\n"
            for node in unconnected_nodes:
                warning_message += f"- Node: {node.title}\n"
            self.showWarningMessage(warning_message)
        
        if len(self.node_list) != len(unconnected_nodes):
            root_node = next((node for node in self.node_list if node not in unconnected_nodes), None)
            if root_node:
                self.root = root_node.get_pytrees()
                self.bt_tree = pt.trees.BehaviourTree(self.root)
    
    def printConnections(self):
        current_node_editor = self.getCurrentNodeEditorWidget()
        if current_node_editor:
            self.print_node_connections(current_node_editor.scene)

    def print_node_connections(self, scene):
        for node in scene.nodes:
            for socket in node.inputs:
                for edge in socket.edges:
                    if edge.start_socket.node != node:
                        connected_node = edge.start_socket.node
                        print(f"Node '{node.title}' is connected to Node '{connected_node.title}' (input)")
            for socket in node.outputs:
                for edge in socket.edges:
                    if edge.end_socket.node != node:
                        connected_node = edge.end_socket.node
                        print(f"Node '{node.title}' is connected to Node '{connected_node.title}' (output)")    

    def onRunOnce(self):
        if self.bt_tree is None:
            self.onBuild()
            
        self.bt_tree.root.tick_once()
        current_node_editor = self.getCurrentNodeEditorWidget()
        self.node_list = current_node_editor.scene.nodes[:] 
        self.update_node_colors()
        root_status = self.bt_tree.root.status
        self.iterations = 0
        self.max_iterations = 50
        self.iterations += 1
        if self.iterations >= self.max_iterations or root_status != pt.common.Status.RUNNING:
            self.stopRun()

    def onRun(self):
        self.timer.timeout.connect(self.onRunOnce) 

        self.timer.start(500)  # Timer calls onRunOnce every 200 milliseconds

    def stopRun(self):
        self.timer.stop()
            
    def onPause(self):
        self.timer.stop()
    
    def onReset(self):
        current_node_editor = self.getCurrentNodeEditorWidget()
        self.node_list = current_node_editor.scene.nodes[:]
        for node in self.node_list:
            content_widget = node.grNode.content
            content_widget.setStyleSheet("background-color: default;")
        root_node = self.getCurrentNodeEditorWidget().scene.nodes[0]        
        self.root=root_node.get_pytrees()
        self.bt_tree = pt.trees.BehaviourTree(self.root)
         
                
    def onFileSaveAs(self):
        current_nodeeditor = self.getCurrentNodeEditorWidget()
        if current_nodeeditor is not None:
            fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file', self.getFileDialogDirectory(), self.getFileDialogFilter())
            if fname == '': return False

            self.onBeforeSaveAs(current_nodeeditor, fname)
            current_nodeeditor.fileSave(fname)
            self.statusBar().showMessage("Successfully saved as %s" % current_nodeeditor.filename, 5000)

            if hasattr(current_nodeeditor, "setTitle"): current_nodeeditor.setTitle()
            else: self.setTitle()
            return True

    def onBeforeSaveAs(self, current_nodeeditor: 'NodeEditorWidget', filename: str):
        pass

    def onEditUndo(self):
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.history.undo()

    def onEditRedo(self):
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.history.redo()

    def onEditDelete(self):
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.getView().deleteSelected()

    def onEditCut(self):
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete=True)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete=False)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        if self.getCurrentNodeEditorWidget():
            raw_data = QApplication.instance().clipboard().text()

            try:
                data = json.loads(raw_data, encoding='utf-8')
            except ValueError as e:
                print("Pasting of not valid json data!", e)
                return

            if 'nodes' not in data:
                print("JSON does not contain any nodes!")
                return

            return self.getCurrentNodeEditorWidget().scene.clipboard.deserializeFromClipboard(data)

    def getCurrentNodeEditorWidget(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e: dumpException(e)

    def onFileOpen(self):
        self.bt_tree = None
        fnames, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file', self.getFileDialogDirectory(), self.getFileDialogFilter())

        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        nodeeditor = CalculatorSubWindow()
                        if nodeeditor.fileLoad(fname):
                            self.statusBar().showMessage("File %s loaded" % fname, 5000)
                            nodeeditor.setTitle()
                            subwnd = self.createMdiChild(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e: dumpException(e)

    def about(self):
        QMessageBox.about(self, "About BT NodeEditor","Mail me for help")

    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)

        self.editMenu.aboutToShow.connect(self.updateEditMenu)
        
        spacer = QWidgetAction(self)
        spacer.setSeparator(True)
        self.menuBar().addAction(spacer)
        
    def updateMenus(self):
        active = self.getCurrentNodeEditorWidget()
        hasMdiChild = (active is not None)

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setVisible(hasMdiChild)

        self.updateEditMenu()

    def updateEditMenu(self):
        try:
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)

            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e: dumpException(e)

    def updateWindowMenu(self):
        self.windowMenu.clear()

        toolbar_nodes = self.windowMenu.addAction("Nodes Toolbar")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)
        toolbar_nodes.setChecked(self.nodesDock.isVisible())

        toolbar_simulation = self.windowMenu.addAction("Simulation Dock")
        toolbar_simulation.setCheckable(True)
        toolbar_simulation.triggered.connect(self.toggleSimulation)
        toolbar_simulation.setChecked(self.simulationDock.isVisible())
        
        self.windowMenu.addSeparator()

        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    def createNodesDock(self):
        self.nodesListWidget = QDMDragListbox()

        self.nodesDock = QDockWidget("Nodes")
        self.nodesDock.setWidget(self.nodesListWidget)
        self.nodesDock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock) 

    def resizeEvent(self, event):
        super().resizeEvent(event)         

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else CalculatorSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)