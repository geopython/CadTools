# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

class ArcIntersection: 
    def intersectionPoint(p1,  p2,  r1,  r2):
        x1 = p1.x()
        x2 = p2.x()
        y1 = p1.y()
        y2 = p2.y()        
        
        r1 = abs(r1)
        r2 = abs(r2)    

        # no intersection
        abc = ( (x2 - x1)**2 + (y2 - y1)**2 )**0.5
        #QMessageBox.information(None,  "Cancel",  str(abc))
        # within
        if abc <= abs(r1 - r2):
            QMessageBox.information(None,  "Cancel",  str("No intersection found."))
            return 0
        # outside
        if abc > abs(r1 + r2):
            QMessageBox.information(None,  "Cancel",  str("No intersection found."))
            return 0
        # infinite
        if((x1 - x2 == 0) and (y1 - y2 == 0)):
            QMessageBox.information(None,  "Cancel",  str("No intersection found."))
            return 0  
         
        final1 = QgsPoint()
        final2 = QgsPoint()
        
        if x1 == x2:
            a = (x1 - x2)/(y2 - y1)
            b = ( (r1*r1 - r2*r2)- (y1*y1 - y2*y2) - (x1*x1 - x2*x2)  )/(2*y2 - 2*y1)
            e = a*a+1
            f = (2*a*(b-y1))-(2*x1)
            g = (b-y1)*(b-y1) -r1*r1 + x1*x1;

            resX1 = (-f + (f*f - 4*e*g)**0.5 )/(2*e);
            resX2 = (-f - (f*f - 4*e*g)**0.5 )/(2*e);
            resY1 = resX1 * a + b;
            resY2 = resX2 * a + b;  
           
            final1.setX(resX1)
            final1.setY(resY1)
            final2.setX(resX2)
            final2.setY(resY2)
            
            return [final1,  final2]

        else: 
            a = (y1 - y2)/(x2 - x1);
            b = ( (r1*r1 - r2*r2)- (x1*x1 - x2*x2) -  (y1*y1 - y2*y2)  )/(2*x2 - 2*x1);
            e = a*a+1;
            f = (2*a*(b-x1))-(2*y1);
            g = (b-x1)*(b-x1) -r1*r1 + y1*y1;
            
            resY1 = (-f + (f*f - 4*e*g)**0.5 ) / (2*e)
            resY2 = (-f - (f*f - 4*e*g)**0.5 ) / (2*e)
            resX1 = resY1 * a + b
            resX2 = resY2 * a + b
            
            final1.setX(resX1)
            final1.setY(resY1)
            final2.setX(resX2)
            final2.setY(resY2)            
            
            return [final1,  final2]
            
        
    def abs(self,  a):
        if a < 1:
            a = a * -1
        return a
        
    intersectionPoint = staticmethod(intersectionPoint)
