# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import math

class Azimuth: 
    def calculate(p1,  p2):
        dx = p2.x()-p1.x()
        dy = p2.y()-p1.y()
        
        if dx == 0 and dy ==0:
            return None
        
        if dy == 0:
            if dx > 0:
                return math.pi / 2
            else:
                return 3 * math.pi / 2
        
        if dx == 0:
            if p1.y() < p2.y():
                return 0
            else:
                return math.pi

        if dx > 0 and dy > 0:
            return math.atan(dx/dy)
        elif dx > 0 and dy < 0:
            return math.atan(dx/dy) + math.pi
        elif dx < 0 and dy < 0:
            return math.atan(dx/dy) + math.pi
        else:
            return math.atan(dx/dy) + 2*math.pi        

        
    calculate = staticmethod(calculate)
