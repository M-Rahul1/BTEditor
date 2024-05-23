import os, sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import json
import py_trees as pt

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


class CalculatorWindow(NodeEditorWindow):

    def __init__(self):
        super().__init__()        
        self.status_bar = self.statusBar()        
        
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
        # print("^Called change color to:", color.red(), color.green(), color.blue(), "on edge:", self.edge)
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
        
    def onBuild(self):
        current_node_editor = self.getCurrentNodeEditorWidget()
        self.node_list = current_node_editor.scene.nodes[:]
        for node in self.node_list:
            content_widget = node.grNode.content
            content_widget.setStyleSheet("background-color: lightgrey;")
        root_node = self.getCurrentNodeEditorWidget().scene.nodes[0]        
        self.root=root_node.get_pytrees()
        self.bt_tree = pt.trees.BehaviourTree(self.root)  
        #print(self.bt_tree)   
    
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
    
    def update_node_colors(self):
        for node in self.node_list:
            content_widget = node.grNode.content
            status = node.py_trees_object.status.value
            #logging.info(f'Node {node.op_title}: Status {status}')
            print(f'Node {node.op_title}: Status {status}')
            self.status_bar.showMessage(f'Node : {node.op_title}               Status : {status}')
            if status == 'SUCCESS':
                content_widget.setStyleSheet("background-color: green;")
            elif status == 'RUNNING':
                content_widget.setStyleSheet("background-color: orange;")
            elif status == 'FAILURE':
                content_widget.setStyleSheet("background-color: red;")
            else:
                content_widget.setStyleSheet("background-color: black;")
    
    def onRunOnce(self):
        self.bt_tree.root.tick_once()
        current_node_editor = self.getCurrentNodeEditorWidget()
        self.node_list = current_node_editor.scene.nodes[:] 
        self.update_node_colors()
        
        
    def onRun(self):
        #if self.bt_tree.root.status != pt.common.Status.SUCCESS and self.bt_tree.root.status != pt.common.Status.FAILURE:
        for _ in range(50):
            self.onRunOnce()
            time.sleep(0.2)
            self.update_node_colors()
            
    def onPause(self):
        pass
    
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
        """Handle File Save As operation"""
        current_nodeeditor = self.getCurrentNodeEditorWidget()
        if current_nodeeditor is not None:
            fname, filter = QFileDialog.getSaveFileName(self, 'Save graph to file', self.getFileDialogDirectory(), self.getFileDialogFilter())
            if fname == '': return False

            self.onBeforeSaveAs(current_nodeeditor, fname)
            current_nodeeditor.fileSave(fname)
            self.statusBar().showMessage("Successfully saved as %s" % current_nodeeditor.filename, 5000)

            # support for MDI app
            if hasattr(current_nodeeditor, "setTitle"): current_nodeeditor.setTitle()
            else: self.setTitle()
            return True

    def onBeforeSaveAs(self, current_nodeeditor: 'NodeEditorWidget', filename: str):
        """
        Event triggered after choosing filename and before actual fileSave(). We are passing current_nodeeditor because
        we will loose focus after asking with QFileDialog and therefore getCurrentNodeEditorWidget will return None
        """
        pass

    def onEditUndo(self):
        """Handle Edit Undo operation"""
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.history.undo()

    def onEditRedo(self):
        """Handle Edit Redo operation"""
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.history.redo()

    def onEditDelete(self):
        """Handle Delete Selected operation"""
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.getView().deleteSelected()

    def onEditCut(self):
        """Handle Edit Cut to clipboard operation"""
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete=True)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        """Handle Edit Copy to clipboard operation"""
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(delete=False)
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        """Handle Edit Paste from clipboard operation"""
        if self.getCurrentNodeEditorWidget():
            raw_data = QApplication.instance().clipboard().text()

            try:
                data = json.loads(raw_data, encoding='utf-8')
            except ValueError as e:
                print("Pasting of not valid json data!", e)
                return

            # check if the json data are correct
            if 'nodes' not in data:
                print("JSON does not contain any nodes!")
                return

            return self.getCurrentNodeEditorWidget().scene.clipboard.deserializeFromClipboard(data)


    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
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
        fnames, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file', self.getFileDialogDirectory(), self.getFileDialogFilter())

        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
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
        # print("update Menus")
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
            # print("update Edit Menu")
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
        

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else CalculatorSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
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