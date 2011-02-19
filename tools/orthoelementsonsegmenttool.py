# -*- coding: latin1 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


# Initialize Qt resources from file resources.py
from cadtools import resources

#Import own classes and tools
#from vertexandsegmentfindertool import VertexAndSegmentFinderTool
from threevertexfindertool import ThreeVertexFinderTool
from lineintersection import LineIntersection
import cadutils

class OrthoElementsOnSegmentTool:
    
        def __init__(self, iface,  toolBar):
            # Save reference to the QGIS interface
            self.iface = iface
            self.canvas = self.iface.mapCanvas()
            
            # Points from Vertex and Segment
            self.p1 = None
            self.p2 = None
            self.p3 = None
                            
            # Create actions 
            self.act_ortholineandpoint = QAction(QIcon(":/plugins/cadtools/icons/orthopointandline.png"),  "Orthogonal Line and Intersection Point",  self.iface.mainWindow())
            self.act_selectvertexandline = QAction(QIcon(":/plugins/cadtools/icons/selectthreevertex.png"),  "Select Vertex Points",  self.iface.mainWindow())
            self.act_selectvertexandline.setCheckable(True)   
      
            # Connect to signals for button behaviour      
            QObject.connect(self.act_ortholineandpoint,  SIGNAL("triggered()"),  self.ortholineandpoint)
            QObject.connect(self.act_selectvertexandline,  SIGNAL("triggered()"),  self.selectvertexandline)
            QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)

            toolBar.addSeparator()
            toolBar.addAction(self.act_selectvertexandline)
            toolBar.addAction(self.act_ortholineandpoint)
                        
            # Get the tool
            self.tool = ThreeVertexFinderTool(self.canvas)           
            
        def selectvertexandline(self):
            mc = self.canvas
            layer = mc.currentLayer()

            # Set VertexAndSegmentFinderTool as current tool
            mc.setMapTool(self.tool)
            self.act_selectvertexandline.setChecked(True)                    
            
            #Connect to the VertexAndSegmentFinderTool
            QObject.connect(self.tool, SIGNAL("vertexFound(PyQt_PyObject)"), self.storeVertex)


        def ortholineandpoint(self):

            if self.p1 == None or self.p2 == None or self.p3 == None:
                QMessageBox.information(None,  "Cancel",  "Not enough objects selected.")
            else:
                # Intersection of the selected segment and the orthogonal line through the selected point
                # Selektierter Punkt ist Aufpunkt (= p1)
                # Richtungsvektor ist der Vektor, der rechwinklig zum Differenzvektor 
                # (gebildet aus den beiden Segmentpunkten) liegt (-> x/y vertauschen).
                
                xp = self.p1.x() + (self.p3.y()-self.p2.y()) 
                yp = self.p1.y() - (self.p3.x()-self.p2.x())  
                p0 = QgsPoint(xp,  yp)
        
                p = LineIntersection.intersectionPoint(self.p1, p0,  self.p2,  self.p3)
                line = [self.p1, p]     
                if p <> None:
                    
                    # Draw the point
                    cadutils.addGeometryToCadLayer(QgsGeometry.fromPoint(p))

                    # Draw the line
                    cadutils.addGeometryToCadLayer(QgsGeometry.fromPolyline(line))
                    self.canvas.refresh()
                    self.unsetTool()
                    self.deactivate()
                    
                else:
                    self.unsetTool()
                    return

            self.p1 = None
            self.p2 = None
            self.p3 = None

        def storeVertex(self, result):
            self.p1 = result[0]
            self.p2 = result[1]
            self.p3 = result[2]

        def unsetTool(self):
            mc = self.canvas
            mc.unsetMapTool(self.tool)                         
            
        def deactivate(self):
            self.p1 = None
            self.p2 = None
            self.p3 = None
            #uncheck the button/menu and get rid off the SFtool signal
            self.act_selectvertexandline.setChecked(False)
