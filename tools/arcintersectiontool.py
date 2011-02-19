# -*- coding: latin1 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


# Initialize Qt resources from file resources.py
from cadtools import resources


#Import own classes and tools
from vertexfindertool import VertexFinderTool
from arcintersectiongui import ArcIntersectionGui
from arcintersection import ArcIntersection
import cadutils

class ArcIntersectionTool:
    
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
            self.act_intersect_arc = QAction(QIcon(":/plugins/cadtools/icons/arcintersectionpoint.png"),  "Arc Intersection",  self.iface.mainWindow())
            self.act_s2v= QAction(QIcon(":/plugins/cadtools/icons/select2vertex.png"),  "Select 2 Vertex Points",  self.iface.mainWindow())
            self.act_s2v.setCheckable(True)      
      
            # Connect to signals for button behaviour      
            QObject.connect(self.act_intersect_arc,  SIGNAL("triggered()"),  self.showDialog)
            QObject.connect(self.act_s2v,  SIGNAL("triggered()"),  self.s2v)
            QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)

            toolBar.addSeparator()
            toolBar.addAction(self.act_s2v)
            toolBar.addAction(self.act_intersect_arc)
                        
            # Get the tool
            self.tool = VertexFinderTool(self.canvas)           
            
        def s2v(self):
            mc = self.canvas
            layer = mc.currentLayer()

            # Set VertexFinderTool as current tool
            mc.setMapTool(self.tool)
            self.act_s2v.setChecked(True)                    
            
            #Connect to the VertexFinderTool
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
                flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
                self.ctrl = ArcIntersectionGui(self.iface.mainWindow(),  flags)
                self.ctrl.initGui()
                self.ctrl.show()
                # connect the signals
                QObject.connect(self.ctrl, SIGNAL("distancesFromPoints(double, double)"), self.calculateArcIntersection)
                QObject.connect(self.ctrl, SIGNAL("closeArcIntersectionGui()"), self.deactivate)
                QObject.connect(self.ctrl, SIGNAL("unsetTool()"), self.unsetTool)
            
            
        def calculateArcIntersection(self,  dist1,  dist2):

            result = ArcIntersection.intersectionPoint(self.p1,  self.p2,  dist1,  dist2)
            if result == 0:
                mc = self.canvas
                mc.unsetMapTool(self.tool)             
                return
            else:
                cadutils.addGeometryToCadLayer(QgsGeometry.fromPoint(result[0]))
                cadutils.addGeometryToCadLayer(QgsGeometry.fromPoint(result[1]))                
                self.canvas.refresh()
                mc = self.canvas
                mc.unsetMapTool(self.tool)     
                
            self.deactivate()
        
        def unsetTool(self):
          mc = self.canvas
          mc.unsetMapTool(self.tool)             
            
        def deactivate(self):
            self.p1 = None
            self.p2 = None
            #uncheck the button/menu and get rid off the SFtool signal
            self.act_s2v.setChecked(False)
            

