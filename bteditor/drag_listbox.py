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
        self.dropdown_icon = QIcon(QPixmap(os.path.join(os.path.dirname(__file__), "data/icons/dropdown.png")))
        self.sortup_icon = QIcon(QPixmap(os.path.join(os.path.dirname(__file__), "data/icons/sortup.png")))
        self.initUI()

    def initUI(self):
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.itemSelectionChanged.connect(self.update_icons)
        self.addMyItems()

    def create_spacer_item(self, height):
        spacer_item = QListWidgetItem("")
        spacer_item.setSizeHint(QSize(0, height))
        spacer_item.setFlags(spacer_item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)
        return spacer_item

    def addMyItems(self):
        # Add spacers
        self.addItem(self.create_spacer_item(10))

        # Add Control section
        self.add_section("Control")
        self.addMyItem("Sequence", icon=os.path.join(os.path.dirname(__file__), "icons/sequence.png"), op_code=SEQUENCE, section_name="Control")
        self.addMyItem("Fallback", icon=os.path.join(os.path.dirname(__file__), "icons/fallback.png"), op_code=FALLBACK, section_name="Control")
        self.addMyItem("Parallel", icon=os.path.join(os.path.dirname(__file__), "icons/parallel.png"), op_code=PARALLEL, section_name="Control")
        self.addItem(self.create_spacer_item(20))
        
        """# Add coffee Condition section
        self.add_section("Condition")
        self.addItem(self.create_spacer_item(10))
        self.addMyItem("Is_coffee_ready?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=IS_COFFEE_READY, section_name="Condition")
        self.addMyItem("Has_coffee?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=HAS_COFFEE, section_name="Condition")
        self.addMyItem("Has_milk?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=HAS_MILK, section_name="Condition")
        self.addMyItem("Has_sugar?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=HAS_SUGAR, section_name="Condition")
        self.addItem(self.create_spacer_item(20))
             
        # Add Action section
        self.add_section("Action")
        self.addItem(self.create_spacer_item(10))
        self.addMyItem("Add_sugar!", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=ADD_SUGAR, section_name="Action")
        self.addMyItem("Add_coffee!", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=ADD_COFFEE, section_name="Action")
        self.addMyItem("Add_milk!", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=ADD_MILK, section_name="Action")   """  
        
        """# Add ai car Condition section
        self.add_section("Condition")
        self.addItem(self.create_spacer_item(10))
        self.addMyItem("No_traffic_light?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=NO_TRAFFIC_LIGHT, section_name="Condition")
        self.addMyItem("Light_is_red?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=LIGHT_IS_RED, section_name="Condition")
        self.addMyItem("Light_is_green?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=LIGHT_IS_GREEN, section_name="Condition")
        self.addMyItem("Light_is_yellow?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=LIGHT_IS_YELLOW, section_name="Condition")
        self.addMyItem("Within_lane?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=WITHIN_LANE, section_name="Condition")
        self.addItem(self.create_spacer_item(20))
        
        # Add Action section
        self.add_section("Action")
        self.addItem(self.create_spacer_item(10))
        self.addMyItem("Stop", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=STOP, section_name="Action")
        self.addMyItem("Proceed", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=PROCEED, section_name="Action")
        self.addMyItem("Caution", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=CAUTION, section_name="Action")
        self.addMyItem("Move_into_lane", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=MOVE_INTO_LANE, section_name="Action")
        self.addMyItem("Keep_driving", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=KEEP_DRIVING, section_name="Action")"""
        
        """# Add healthCare Condition section
        self.add_section("Condition")
        self.addItem(self.create_spacer_item(10))
        self.addMyItem("No_emergency?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=NO_EMERGENCY, section_name="Condition")
        self.addMyItem("Medicine_with_patient?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=MEDICINE_WITH_PATIENT, section_name="Condition")
        self.addMyItem("Robot_at_medicine?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=ROBOT_AT_MEDICINE, section_name="Condition")
        self.addMyItem("Robot_at_patient?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=ROBOT_AT_PATIENT, section_name="Condition")        
        self.addItem(self.create_spacer_item(20))
        
        self.add_section("Action")
        self.addItem(self.create_spacer_item(10))
        self.addMyItem("Assist_patient", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=ASSIST_PATIENT, section_name="Action")
        self.addMyItem("Move_to_medicine", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=MOVE_TO_MEDICINE, section_name="Action")
        self.addMyItem("Pick_up_medicine", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=PICK_UP_MEDICINE, section_name="Action")
        self.addMyItem("Move_to_patient", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=MOVE_TO_PATIENT, section_name="Action")
        self.addMyItem("Deliver_medicine", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=DELIVER_MEDICINE, section_name="Action")"""
        
        """# Add Energy Management for Hospital 
        self.add_section("Condition")
        self.addItem(self.create_spacer_item(10))
        self.addMyItem("Critical_system_power?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=CRITICAL_SYSTEM_POWER, section_name="Condition")
        self.addMyItem("No_excess_renewable_energy?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=NO_EXCESS_RENEWABLE_ENERGY, section_name="Condition")
        self.addMyItem("Non_critical_system_power?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=NON_CRITICAL_SYSTEM_POWER, section_name="Condition")
        self.addMyItem("No_stored_energy_available?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=NO_STORED_ENERGY_AVAILABLE, section_name="Condition")
        self.addItem(self.create_spacer_item(20))
        
        self.add_section("Action")
        self.addItem(self.create_spacer_item(10))
        self.addMyItem("Power_critical_system", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=POWER_CRITICAL_SYSTEM, section_name="Action")
        self.addMyItem("Notify_admin", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=NOTIFY_ADMIN, section_name="Action")
        self.addMyItem("Store_excess_energy", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=STORE_EXCESS_ENERGY, section_name="Action")
        self.addMyItem("Power_non_critical_system", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=POWER_NON_CRITICAL_SYSTEM, section_name="Action")
        self.addMyItem("Use_stored_energy", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=USE_STORED_ENERGY, section_name="Action")"""
        
        self.add_section("Condition")
        self.addItem(self.create_spacer_item(10))
        self.addMyItem("Parts_in_assembly?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=PARTS_IN_ASSEMBLY, section_name="Condition")
        self.addMyItem("Product_assembled?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=PRODUCT_ASSSEMBLED, section_name="Condition")
        self.addMyItem("Products_stored?", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=PRODUCTS_STORED, section_name="Condition")
        self.addItem(self.create_spacer_item(20))
        
        self.add_section("Action")
        self.addItem(self.create_spacer_item(10))
        self.addMyItem("Pick_parts", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=PICK_PARTS, section_name="Action")
        self.addMyItem("Place_parts_in_assembly", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=PLACE_PARTS_IN_ASSEMBLY, section_name="Action")
        self.addMyItem("Assemble_product", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=ASSEMBLE_PRODUCT, section_name="Action")
        self.addMyItem("Store_product", icon=os.path.join(os.path.dirname(__file__), "icons/action.png"), op_code=STORE_PRODUCT, section_name="Action")       
        
          
        
    def add_section(self, section_name):        
        section_header = QListWidgetItem(section_name)
        section_header.setFont(QFont("Arial", 13, QFont.Bold))
        section_header.setFlags(section_header.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsDragEnabled)
        section_header.setBackground(QBrush(Qt.darkGray))
        section_header.setSizeHint(QSize(section_header.sizeHint().width(), 50))  # Adjust the height as needed
        section_header.setIcon(self.dropdown_icon)
        self.addItem(section_header)
        self.sections[section_name] = section_header
        self.section_states[section_name] = True  # Initially expanded
        
    def addMyItem(self, name, icon=None, op_code=0, section_name=None):
        item = QListWidgetItem(name, self)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(40, 40))
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

    def update_icons(self):
        for section_name, section_header in self.sections.items():
            if section_header.isSelected():
                section_header.setIcon(self.sortup_icon)
            else:
                section_header.setIcon(self.dropdown_icon)

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
