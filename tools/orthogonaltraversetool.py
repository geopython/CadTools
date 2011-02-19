# -*- coding: latin1 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# Initialize Qt resources from file resources.py
from cadtools import resources

#Import own classes and tools
from vertexfindertool import VertexFinderTool
from orthogonaltraversegui import OrthogonalTraverseGui
from orthogonaltraverse import OrthogonalTraverse
import cadutils
import math

class OrthogonalTraverseTool:
    
        def __init__(self, iface,  toolBar):
            # Save reference to the QGIS interface
            self.iface = iface
            self.canvas = self.iface.mapCanvas()
            
            # Points and Markers
            self.p1 = None
            self.p2 = None
            self.m1 = None
            self.m2 = None
            
            # Create actions 
            self.act_showDialog = QAction(QIcon(":/plugins/cadtools/icons/orthogonaltraverse2.png"),  "Orthogonal Traverse",  self.iface.mainWindow())
            self.act_select2vertex= QAction(QIcon(":/plugins/cadtools/icons/select2vertex.png"),  "Select 2 Vertex Points",  self.iface.mainWindow())
            self.act_select2vertex.setCheckable(True)      
      
            # Connect to signals for button behaviour      
            QObject.connect(self.act_showDialog,  SIGNAL("triggered()"),  self.showDialog)
            QObject.connect(self.act_select2vertex,  SIGNAL("triggered()"),  self.select2vertex)
            QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)

            toolBar.addSeparator()
            toolBar.addAction(self.act_select2vertex)            
            toolBar.addAction(self.act_showDialog)

            # Get the tool
            self.tool = VertexFinderTool(self.canvas)    
            
        
        def select2vertex(self):
            mc = self.canvas
            layer = mc.currentLayer()

            # Set VertexFinderTool as current tool
            mc.setMapTool(self.tool)
            self.act_select2vertex.setChecked(True)       
            
            QObject.connect(self.tool, SIGNAL("vertexFound(PyQt_PyObject)"), self.storeVertexPointsAndMarkers)     
            
        def storeVertexPointsAndMarkers(self,  result):
            self.p1 = result[0]
            self.p2 = result[1]
            self.m1 = result[2]
            self.m2 = result[3]
        
        def showDialog(self):
            if self.p1 == None or self.p2 == None:
                QMessageBox.information(None,  "Cancel",  "Not enough vertex selected.")
            else: 
                self.ctrl = OrthogonalTraverseGui(self.iface.mainWindow())
                self.ctrl.initGui(self.p1, self.p2)
                self.ctrl.show()
                
                # Connect the signals
                QObject.connect(self.ctrl, SIGNAL("sendTraverse(QString, double, double, double, double, bool, bool)"), self.calculateTraverse)
                QObject.connect(self.ctrl, SIGNAL("closeOrthogonalTraverseGui()"), self.deactivate)            
                QObject.connect(self.ctrl, SIGNAL("unsetTool()"), self.unsetTool)
                
        def calculateTraverse(self, traverse, x1, y1, x2, y2, adjust, addLine):
            
            # Azimuth Startingpoint to Endpoint
            referenceAzimuth = cadutils.azimuth(QgsPoint(x1,y1), QgsPoint(x2,y2))
            
            # Create the line in a local coordinatesystem:
            # - origin is the starting point
            # - azimuth is 0
            
            line = OrthogonalTraverse.traverse(traverse, 0, 1)
            if line == None:
                print "Line is None!"
            else:
                points = line.asPolyline()
                
                # Azimuth of the new line (first to last point of the line)
                actualAzimuth = cadutils.azimuth( points[0], points[-1] )

                # Difference of reference distance and actual distance
                diff = 100* (cadutils.distance(QgsPoint(x1,y1), QgsPoint(x2,y2)) - cadutils.distance(points[0], points[-1]))
                      
                # number of characters to show as "Fs"
                if diff > 10:
                    digit = math.ceil(math.log10(abs(diff)))
                else:
                    digit = 1
                digit += 3
                if diff < 0:
                    digit += 1
                                        
                # update the difference ("Fs") text in the GUI
                self.ctrl.lineEditFs.setText(str(diff)[:int(digit)] + str( " [cm]"));
                
                # If the OK button was clicked we will rotate and if desired scale/adjust 
                # the line and add it to the map canvas.
                if addLine == True:
                    rotationAngle = actualAzimuth - referenceAzimuth
                    scale = cadutils.distance(QgsPoint(x1,y1), QgsPoint(x2,y2)) / cadutils.distance(points[0], points[-1])
                    
                    print str("scale ") + str(scale)
                    
                    if adjust == True:
                        lineTransformed = cadutils.helmert2d(line, x1, y1, rotationAngle, scale)
                    else:
                        lineTransformed = cadutils.helmert2d(line, x1, y1, rotationAngle, 1.0)
                    
                    if lineTransformed <> None:
                        cadutils.addGeometryToCadLayer(lineTransformed)
                        self.canvas.refresh()
                    else:
                        QMessageBox.information(None,  "Warning", "Error while transforming geometry.")

        def unsetTool(self):
            mc = self.canvas
            mc.unsetMapTool(self.tool)             
            
        def deactivate(self):
            self.p1 = None
            self.p2 = None
            #uncheck the button/menu and get rid off the SFtool signal
            self.act_select2vertex.setChecked(False)
            QObject.disconnect(self.tool, SIGNAL("vertexFound(PyQt_PyObject)"), self.storeVertexPointsAndMarkers)      
            

