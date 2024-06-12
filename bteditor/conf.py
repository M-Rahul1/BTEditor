LISTBOX_MIMETYPE = "application/x-item"

FALLBACK = 1
SEQUENCE = 2
PARALLEL = 3
IS_COFFEE_READY=4
HAS_COFFEE=5
HAS_MILK=6
HAS_SUGAR=7
ADD_COFFEE=8
ADD_MILK=9
ADD_SUGAR=10


NO_EMERGENCY = 11
STOP_VECHILE = 12
ALERT_AUTHORITIES = 13
NO_TRAFFIC_LIGHTS = 14
LIGHT_IS_RED = 15
LIGHT_IS_GREEN = 16
LIGHT_IS_YELLOW = 17
STOP = 18
GO = 19
CAUTION = 20
WITHIN_LANE_MARKINGS = 21
MOVE_INTO_LANE = 22
KEEP_DRIVING = 23


MONITOR_ENERGY_USAGE = 24
USAGE_ABOVE_THRESHOLD = 25
ADJUST_THRESOLD = 26
MAINTAIN_SETTINGS = 27
MONITOR_SENSOR = 28
NO_INTRUSION_DETECTED = 29
LOCK_DOWN_HOUSE = 30
SOUND_ALARM = 31
ALERT_AUTHORITIES = 32



CALC_NODES = {
}


class ConfException(Exception): pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass


def register_node_now(op_code, class_reference):
    if op_code in CALC_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" %(
            op_code, CALC_NODES[op_code]
        ))
    CALC_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator

def get_class_from_opcode(op_code):
    if op_code not in CALC_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return CALC_NODES[op_code]



# import all nodes and register them
from bteditor.nodes import *