# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import math
import cadutils

class OrthogonalTraverse:
    
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        
        
        
    def traverse(trv,  azth,  scale):
##        print "OrthogonalTraverse.traverse"
##        print trv
        meas = str(trv).split()
        
        # List of the points
        coords = []
        
        # Startingpoint
        p0 = QgsPoint(0,0)
        coords.append(p0)
        
        p1 = QgsPoint(0,abs(float(meas[0])))
        coords.append(p1)

        for i in range(len(meas)):
            if i > 0:
                azi =  cadutils.azimuth(p0, p1)
                if azi == 0 or azi == 2*math.pi:
                    p0 = p1
                    p1 = QgsPoint( p0.x()+float(meas[i]), p0.y() )
                    coords.append(p1)
                elif azi == math.pi / 2:
                    p0 = p1
                    p1 = QgsPoint( p0.x(),  p0.y() - float(meas[i]))
                    coords.append(p1) 
                elif azi == math.pi:
                    p0 = p1
                    p1 = QgsPoint( p0.x() - float(meas[i]), p0.y() )
                    coords.append(p1)
                elif azi == 3*math.pi/2:
                    p0 = p1
                    p1 = QgsPoint( p0.x(), p0.y() + float(meas[i]))

        if len(coords) > 0:
            g = QgsGeometry.fromPolyline(coords)
            return g
        else:
            return None
                
    
    traverse = staticmethod(traverse)
    
