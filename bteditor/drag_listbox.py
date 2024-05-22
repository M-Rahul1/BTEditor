import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from bteditor.conf import *
from nodeeditor.utils import dumpException

class QDMDragListbox(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sections = {}
        self.section_states = {}
        self.initUI()

    def initUI(self):
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.addMyItems()

    def addMyItems(self):
        
        spacer_item = QListWidgetItem("")
        spacer_item.setSizeHint(QSize(0, 5))  # Adjust the height as needed
        spacer_item.setFlags(spacer_item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)
        self.addItem(spacer_item)
        
        self.addMyItem("Root", icon=os.path.join(os.path.dirname(__file__), "icons/root.png"), op_code=ROOT, section_name="Task 1")
        self.addMyItem("Sequence", icon=os.path.join(os.path.dirname(__file__), "icons/sequence.png"), op_code=SEQUENCE, section_name="Task 1")
        self.addMyItem("Fallback", icon=os.path.join(os.path.dirname(__file__), "icons/fallback.png"), op_code=FALLBACK, section_name="Task 1")
        self.addMyItem("Parallel", icon=os.path.join(os.path.dirname(__file__), "icons/parallel.png"), op_code=PARALLEL, section_name="Task 1")
        
        spacer_item = QListWidgetItem("")
        spacer_item.setSizeHint(QSize(0, 20))  # Adjust the height as needed
        spacer_item.setFlags(spacer_item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)
        self.addItem(spacer_item)
        
        self.add_section("Task 1")
        
        spacer_item = QListWidgetItem("")
        spacer_item.setSizeHint(QSize(0, 10))  # Adjust the height as needed
        spacer_item.setFlags(spacer_item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)
        self.addItem(spacer_item)
        
        self.addMyItem("CUBE2_DELIVERED?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=CUBE2_DELIVERED, section_name="Task 1")
        self.addMyItem("Cube2_in_hand?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=CUBE2_IN_HAND, section_name="Task 1")
        self.addMyItem("Robot_at_cube2?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=ROBOT_AT_CUBE2, section_name="Task 1")
        self.addMyItem("Move_to_cube2!", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=MOVE_TO_CUBE2, section_name="Task 1")
        self.addMyItem("Pick_cube2!", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=PICK_CUBE2, section_name="Task 1")

        self.add_section("Task 2")
        
        spacer_item = QListWidgetItem("")
        spacer_item.setSizeHint(QSize(0, 10))  # Adjust the height as needed
        spacer_item.setFlags(spacer_item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)
        self.addItem(spacer_item)
        
        self.addMyItem("Robot_at_delivery?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=ROBOT_AT_DELIVERY, section_name="Task 2")
        self.addMyItem("Move_to_delivery!", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=MOVE_TO_DELIVERY, section_name="Task 2")
        self.addMyItem("Place_cube2!", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=PLACE_CUBE2, section_name="Task 2")

    def add_section(self, section_name):
        if self.sections:
            # Add a spacer item for vertical spacing
            spacer_item = QListWidgetItem("")
            spacer_item.setSizeHint(QSize(0, 20))  # Adjust the height as needed
            spacer_item.setFlags(spacer_item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)
            self.addItem(spacer_item)

        section_header = QListWidgetItem(section_name)
        section_header.setFlags(section_header.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsDragEnabled)
        section_header.setBackground(QBrush(Qt.lightGray))
        section_header.setSizeHint(QSize(section_header.sizeHint().width(), 30))  # Adjust the height as needed
        self.addItem(section_header)
        self.sections[section_name] = section_header
        self.section_states[section_name] = True  # Initially expanded

    def addMyItem(self, name, icon=None, op_code=0, section_name=None):
        item = QListWidgetItem(name, self)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(32, 32))
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)

        if section_name in self.sections:
            index = self.row(self.sections[section_name]) + 1
            while index < self.count() and not self.item(index).flags() & Qt.ItemIsSelectable:
                index += 1
            self.insertItem(index, item)
        else:
            self.addItem(item)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if item and item in self.sections.values():
            section_name = item.text()
            self.toggle_section(section_name)
        super().mousePressEvent(event)

    def toggle_section(self, section_name):
        state = self.section_states[section_name]
        start_index = self.row(self.sections[section_name]) + 1
        while start_index < self.count() and self.item(start_index).text() not in self.sections:
            self.item(start_index).setHidden(state)
            start_index += 1
        self.section_states[section_name] = not state

    def startDrag(self, *args, **kwargs):
        try:
            item = self.currentItem()
            op_code = item.data(Qt.UserRole + 1)
            pixmap = QPixmap(item.data(Qt.UserRole))

            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt(op_code)
            dataStream.writeQString(item.text())

            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(int(pixmap.width() / 2), int(pixmap.height() / 2)))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)
        except Exception as e:
            dumpException(e)
