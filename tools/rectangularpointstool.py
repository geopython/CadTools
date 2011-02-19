# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

# Initialize Qt resources from file resources.py
from cadtools import resources

#Import own classes and tools
from rectangularpointsgui import RectangularPointsGui
from singlesegmentfindertool import SingleSegmentFinderTool
from rectangularpoint import RectangularPoint
import cadutils

class RectangularPointsTool():
    
        def __init__(self, iface,  toolBar):
            # Save reference to the QGIS interface
            self.iface = iface
            self.canvas = self.iface.mapCanvas()
            
            # the 2 points of the segment
            # p1 is always the left point
            self.p1 = None
            self.p2 = None
                
            # Create actions 
            self.act_rectpoints = QAction(QIcon(":/plugins/cadtools/icons/orthopoint.png"),  "Rectangular Points",  self.iface.mainWindow())
            self.act_selectlinesegment= QAction(QIcon(":/plugins/cadtools/icons/select1line_v2.png"),  "Select Line Segments",  self.iface.mainWindow())
            self.act_selectlinesegment.setCheckable(True)            
            
            # Connect to signals for button behaviour
            QObject.connect(self.act_rectpoints,  SIGNAL("triggered()"),  self.showDialog) 
            QObject.connect(self.act_selectlinesegment,  SIGNAL("triggered()"),  self.selectlinesegment)   
            QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)
            
            # Add actions to the toolbar
            toolBar.addSeparator()
            toolBar.addAction(self.act_selectlinesegment)
            toolBar.addAction(self.act_rectpoints)
            
            # Get the tool
            self.tool = SingleSegmentFinderTool(self.canvas)
            
        def showDialog(self):
            if self.p1 == None or self.p2 == None:
                QMessageBox.information(None,  "Cancel",  "No segment selected.")
            else:
                flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint 
                self.ctrl = RectangularPointsGui(self.iface.mainWindow(),  flags)
                self.ctrl.initGui()
                self.ctrl.show()
                # connect the signals
                QObject.connect(self.ctrl, SIGNAL("coordSegments(double, double, bool)"), self.calculateRectangularPoint)
                QObject.connect(self.ctrl, SIGNAL("closeRectangularPointsGui()"), self.deactivate)            
                QObject.connect(self.ctrl, SIGNAL("unsetTool()"), self.unsetTool)
                         
        def calculateRectangularPoint(self, dX, dY,  inverse):
            # I still don't get it.....
            pt1 = QgsPoint()
            pt1.setX(self.p1.x())
            pt1.setY(self.p1.y())
            pt2 = QgsPoint()
            pt2.setX(self.p2.x())
            pt2.setY(self.p2.y())            
            
            # Calculate the new (rectangular) Point
            result = RectangularPoint.point(pt1, pt2, dX, dY, inverse)
            
            if result == 0:
                mc = self.canvas
                mc.unsetMapTool(self.tool)             
                return
            else:
                cadutils.addGeometryToCadLayer(QgsGeometry.fromPoint(result))
                self.canvas.refresh()
                
            self.p1 = pt1
            self.p2 = pt2
            
        # Select  Line Segment
        def selectlinesegment(self):
            pass
            mc = self.canvas
            layer = mc.currentLayer()

            # Set SegmentFinderTool as current tool
            mc.setMapTool(self.tool)
            self.act_selectlinesegment.setChecked(True)        
                    
            #Connect to the SegmentFinderTool
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
        
        def unsetTool(self):
            mc = self.canvas
            mc.unsetMapTool(self.tool)             
                
        def deactivate(self):
            #QMessageBox.information(None,  "Cancel",  str(self.ctrl))
            self.p1 = None
            self.p2 = None
                    
            #uncheck the button/menu and get rid off the SSFtool signal
            self.act_selectlinesegment.setChecked(False)
            QObject.disconnect(self.tool, SIGNAL("segmentFound(PyQt_PyObject)"), self.storeSegmentPoints)                  
