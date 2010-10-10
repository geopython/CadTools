# -*- coding: latin1 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# Initialize Qt resources from file resources.py
import resources

#Import own classes and tools
from singlesegmentfindertool import SingleSegmentFinderTool
from parallellinegui import ParallelLineGui
from parallelline import ParallelLine
import cadutils

class ParallelLineTool:
    
        def __init__(self, iface,  toolBar):
            # Save reference to the QGIS interface
            self.iface = iface
            self.canvas = self.iface.mapCanvas()
            
            # the 2 points of the segment
            # p1 is always the left point
            self.p1 = None
            self.p2 = None
            
            # Points and Markers
#            self.p1 = None
#            self.p2 = None
#            self.m1 = None
#            self.m2 = None
            
            # Create actions 
            self.action_selectline = QAction(QIcon(":/plugins/cadtools/icons/select1line.png"),  "Select one linesegment",  self.iface.mainWindow())
            self.action_parallelline = QAction(QIcon(":/plugins/cadtools/icons/parallel.png"),  "Create parallel line",  self.iface.mainWindow())
            self.action_selectline.setCheckable(True)      
      
            # Connect to signals for button behaviour      
            QObject.connect(self.action_selectline,  SIGNAL("triggered()"),  self.selectLineSegment)
            QObject.connect(self.action_parallelline,   SIGNAL("triggered()"),  self.showDialog)
            QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)

            toolBar.addSeparator()
            toolBar.addAction(self.action_selectline)
            toolBar.addAction(self.action_parallelline)
                        
            # Get the tool
            self.tool = SingleSegmentFinderTool(self.canvas)           

        def selectLineSegment(self):
            mc = self.canvas
            layer = mc.currentLayer()

            # Set SingleSegmentFinder as current tool
            mc.setMapTool(self.tool)
            self.action_selectline.setChecked(True)      

            # Connect to the SingleSegmentFinderTool
            QObject.connect(self.tool, SIGNAL("segmentFound(PyQt_PyObject)"), self.storeSegmentPoints)

        def storeSegmentPoints(self,  result):
            if result[0].x() < result[1].x():
                self.p1 = result[0]
                self.p2 = result[1]
            elif result[0].x() == result[1].x():
                self.p1 = result[0]
                self.p2 = result[1]
            else:
                self.p1 = result[1]
                self.p2 = result[0]        



#            #Connect to the VertexFinderTool
#            QObject.connect(self.tool, SIGNAL("vertexFound(PyQt_PyObject)"), self.storeVertexPointsAndMarkers)
#
#        def storeVertexPointsAndMarkers(self,  result):
#            self.p1 = result[0]
#            self.p2 = result[1]
#            self.m1 = result[2]
#            self.m2 = result[3]
#    
        def showDialog(self):
            if self.p1 == None or self.p2 == None:
                QMessageBox.information(None,  "Cancel",  "No linesegment selected.")
            else:
                flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
                self.ctrl = ParallelLineGui(self.iface.mainWindow(),  flags)
                self.ctrl.initGui()
                self.ctrl.show()

                QObject.connect(self.ctrl, SIGNAL("okClicked(QString, double)"), self.createParallelLine)
                
                ## Muss anders gemacht werden, will ja nach einmal gleich nochmals verschieben etc. etc....
                #
                #
                #QObject.connect(self.ctrl, SIGNAL("unsetTool()"), self.unsetTool)
            
            
        def createParallelLine(self, method,  distance):
            # We need this because adding a layer to the mapcanvas deletes everything....
            p1 = QgsPoint()
            p2 = QgsPoint()
            
            p1.setX(self.p1.x()) 
            p1.setY(self.p1.y()) 
            p2.setX(self.p2.x()) 
            p2.setY( self.p2.y())             

            print "***************************** asdfasdf"
            print str(method)
            print str(distance)
            
            if method == "fixed":
                
                g = ParallelLine.calculateLine(self.p1,  self.p2,  distance)
                
                cadutils.addGeometryToCadLayer(g)     
                self.canvas.refresh  

                self.p1 = p1
                self.p2 = p2

           #                  result = ArcIntersection.intersectionPoint(self.p1,  self.p2,  dist1,  dist2)
#            if result == 0:
#                mc = self.canvas
#                mc.unsetMapTool(self.tool)             
#                return
#            else:
#                cadutils.addGeometryToCadLayer(QgsGeometry.fromPoint(result[0]))
#                cadutils.addGeometryToCadLayer(QgsGeometry.fromPoint(result[1]))                
#                self.canvas.refresh()
#                mc = self.canvas
#                mc.unsetMapTool(self.tool)     
#                
#            self.deactivate()
        
        def unsetTool(self):
            mc = self.canvas
            mc.unsetMapTool(self.tool)      
            self.action_selectline.setChecked(False)       
            
            print "********************* UNSET"
            
        def deactivate(self):
            self.p1 = None
            self.p2 = None
            self.action_selectline.setChecked(False)       
            

