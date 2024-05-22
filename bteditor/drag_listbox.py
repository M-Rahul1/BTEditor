import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from bteditor.conf import *
from nodeeditor.utils import dumpException


class QDMDragListbox(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # init
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

        self.addMyItems()


    def addMyItems(self):
        self.addMyItem("Sequence", icon=os.path.join(os.path.dirname(__file__), "icons/sequence.png"), op_code=SEQUENCE)
        self.addMyItem("Fallback", icon=os.path.join(os.path.dirname(__file__), "icons/fallback.png"), op_code=FALLBACK)
        self.addMyItem("Parallel", icon=os.path.join(os.path.dirname(__file__), "icons/parallel.png"), op_code=PARALLEL)
        self.addMyItem("CUBE2_DELIVERED", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=CUBE2_DELIVERED)
        self.addMyItem("Cube2_in_hand", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=CUBE2_IN_HAND)
        self.addMyItem("Robot_at_cube2", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=ROBOT_AT_CUBE2)
        self.addMyItem("Move_to_cube2", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=MOVE_TO_CUBE2)
        self.addMyItem("Pick_cube2", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=PICK_CUBE2)
        self.addMyItem("Robot_at_delivery", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=ROBOT_AT_DELIVERY)
        self.addMyItem("Move_to_delivery", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=MOVE_TO_DELIVERY)
        self.addMyItem("Place_cube2", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=PLACE_CUBE2)

    def addMyItem(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self) # can be (icon, text, parent, <int>type)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(32, 32))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        # setup data
        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)


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

        except Exception as e: dumpException(e)