# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

class LineIntersection:
    
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        
        
    # Use following algorithm:
    # A = y2-y1
    # B = x1-x2
    # C = A*x1+B*y1    
    #
    # det = A1*B2 - A2*B1
    # X = (B2*C1 - B1*C2) / det
    # Y = (A1*C2 - A2*C1) / det
        
    def intersectionPoint(p11,  p12,  p21,  p22):

        a1 = p12.y() - p11.y()
        b1 = p11.x() - p12.x()
        c1 = a1*p11.x() + b1*p11.y()
        
        a2 = p22.y() - p21.y()
        b2 = p21.x() - p22.x()
        c2 = a2*p21.x() + b2*p21.y()
        
        det = a1*b2 - a2*b1
        
        p = QgsPoint()
        if det == 0:
            QMessageBox.information(None,  "Cancel",  "No intersection point found.")
            return None
        else:
            x = (b2*c1 - b1*c2) / det
            y = (a1*c2 - a2*c1) / det
            p.setX(x)
            p.setY(y)
            #QMessageBox.information(None,  "Cancel",  str(p.toString()))
            return p
        
    def intersectionLine(p11,  p12,  p21,  p22):   
        p = QgsPoint()
        p = LineIntersection.intersectionPoint(p11,  p12,  p21,  p22)
        #QMessageBox.information(None,  "Cancel",  str(p.toString()))
        if p <> None:
            p1 = LineIntersection.farestVertex(p11,  p12,  p)
            p2 = LineIntersection.farestVertex(p21,  p22,  p)
            
            points =  [p1,  p,  p2]
            
            g = QgsGeometry.fromPolyline(points)
            return g
         
        else:
            return None
            
    def farestVertex(p1,  p2,  p):
        g1 = QgsGeometry.fromPoint(p1)
        g2 = QgsGeometry.fromPoint(p2)
        g = QgsGeometry.fromPoint(p)
        
        d1 = g1.distance(g)
        d2 = g2.distance(g)
        
        if d1 > d2:
            return p1
        else:
            return p2
    
    intersectionPoint = staticmethod(intersectionPoint)
    intersectionLine = staticmethod(intersectionLine)
    farestVertex = staticmethod(farestVertex)
    
