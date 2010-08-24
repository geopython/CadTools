# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

class RectangularPoint:
    
    
    def point(p1, p2, dX, dY,  inverse):
                    
        # Aufpunkt ist p1 (also immer der linke Punkt)
        # Richtungsvektor ist: p2 - p1
        
        if dX == 0:
            if inverse == True:
                pA = QgsPoint()
                pA.setX(p2.x())
                pA.setY(p2.y())
            else:
                pA = QgsPoint()
                pA.setX(p1.x())
                pA.setY(p1.y())
        else:
            dA = ( (p1.x()-p2.x())**2 + (p1.y()-p2.y())**2 )**0.5
            
            if inverse == True:
                xA = p2.x() - dX*(p2.x()-p1.x())/dA 
                yA =  p2.y() - dX*(p2.y()-p1.y())/dA  
                pA = QgsPoint(xA,  yA)    
            else:
                xA = p1.x() + dX*(p2.x()-p1.x())/dA 
                yA =  p1.y() + dX*(p2.y()-p1.y())/dA  
                pA = QgsPoint(xA,  yA)    
        
        
        # Aufpunkt ist neu pA
        # Richtungsvektor ist p1 - pA jedoch mit x/y vertauscht
        
        if dX == 0:
            if inverse == True:      
                dO = ( (p1.x()-p2.x())**2 + (p1.y()-p2.y())**2 )**0.5
                xO = p2.x() + dY*(p2.y()-p1.y())/dO 
                yO = p2.y() - dY*(p2.x()-p1.x())/dO  
                pO = QgsPoint(xO,  yO)          
            else:
                dO = ( (p1.x()-p2.x())**2 + (p1.y()-p2.y())**2 )**0.5
                xO = p1.x() + dY*(p1.y()-p2.y())/dO 
                yO = p1.y() - dY*(p1.x()-p2.x())/dO  
                pO = QgsPoint(xO,  yO)          
            
        else:
            dO = dX
            if inverse == True:
                xO = pA.x() + dY*(p2.y()-pA.y())/dO 
                yO = pA.y() - dY*(p2.x()-pA.x())/dO  
                pO = QgsPoint(xO,  yO)          
            else:
                xO = pA.x() + dY*(p1.y()-pA.y())/dO 
                yO = pA.y() - dY*(p1.x()-pA.x())/dO  
                pO = QgsPoint(xO,  yO)          
        
        return pO
        
    point = staticmethod(point)
