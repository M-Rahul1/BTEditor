import math
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainterPath


EDGE_CP_ROUNDNESS = 100     #: Bezier control point distance on the line


class GraphicsEdgePathBase:
    """Base Class for calculating the graphics path to draw for an graphics Edge"""

    def __init__(self, owner: 'QDMGraphicsEdge'):
        # keep the reference to owner GraphicsEdge class
        self.owner = owner

    def calcPath(self):
        """Calculate the Direct line connection

        :returns: ``QPainterPath`` of the graphics path to draw
        :rtype: ``QPainterPath`` or ``None``
        """
        return None


class GraphicsEdgePathDirect(GraphicsEdgePathBase):
    """Direct line connection Graphics Edge"""
    def calcPath(self) -> QPainterPath:
        """Calculate the Direct line connection

        :returns: ``QPainterPath`` of the direct line
        :rtype: ``QPainterPath``
        """
        path = QPainterPath(QPointF(self.owner.posSource[0], self.owner.posSource[1]))
        path.lineTo(self.owner.posDestination[0], self.owner.posDestination[1])
        return path


class GraphicsEdgePathBezier(GraphicsEdgePathBase):
    """Cubic line connection Graphics Edge"""
    def calcPath(self) -> QPainterPath:
        """Calculate the cubic Bezier line connection with 2 control points

        :returns: ``QPainterPath`` of the cubic Bezier line
        :rtype: ``QPainterPath``
        """
        s = self.owner.posSource
        d = self.owner.posDestination
        dist = (d[1] - s[1]) * 0.5  # Calculate half of the vertical distance

        cpx_s = 0
        cpx_d = 0
        cpy_s = +dist  # Adjust control point for source position
        cpy_d = -dist  # Adjust control point for destination position

        if self.owner.edge.start_socket is not None:
            ssin = self.owner.edge.start_socket.is_input
            ssout = self.owner.edge.start_socket.is_output

            if (s[1] > d[1] and ssout) or (s[1] < d[1] and ssin):  # Check direction
                cpx_d = (
                    (s[0] - d[0]) / math.fabs(
                        (s[0] - d[0]) if (s[0] - d[0]) != 0 else 0.00001
                    )
                ) * EDGE_CP_ROUNDNESS  # Adjust control point for destination position
                cpx_s = (
                    (d[0] - s[0]) / math.fabs(
                        (d[0] - s[0]) if (d[0] - s[0]) != 0 else 0.00001
                    )
                ) * EDGE_CP_ROUNDNESS  # Adjust control point for source position

        path = QPainterPath(QPointF(self.owner.posSource[0], self.owner.posSource[1]))
        path.cubicTo(s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.owner.posDestination[0], self.owner.posDestination[1])

        return path
