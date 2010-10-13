# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

class ParallelLine: 
    def calculateLine(p1,  p2, dist):
        
        if dist == 0:
            points = [p1,  p2]
            g = QgsGeometry.fromPolyline(points)
            return g
    
        dn = ( (p1.x()-p2.x())**2 + (p1.y()-p2.y())**2 )**0.5
        x3 = p1.x() + dist*(p1.y()-p2.y()) / dn
        y3 = p1.y() - dist*(p1.x()-p2.x()) / dn  
        p3 = QgsPoint(x3,  y3)       
      
        x4 = p2.x() + dist*(p1.y()-p2.y()) / dn
        y4 = p2.y() - dist*(p1.x()-p2.x()) / dn  
        p4 = QgsPoint(x4,  y4)       
        
        points =  [p3,  p4]
        g = QgsGeometry.fromPolyline(points)
        
        return g


        
    calculateLine = staticmethod(calculateLine)
