# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# Initialize Qt resources from file resources.py
from cadtools import resources

#Import own classes and tools
from segmentfindertool import SegmentFinderTool
from lineintersection import LineIntersection
import cadutils

class LineIntersectionTool():
    
        def __init__(self, iface,  toolBar):
            # Save reference to the QGIS interface
            self.iface = iface
            self.canvas = self.iface.mapCanvas()
            
            # the 4 points of the 2 segments
            self.p11 = None
            self.p12 = None
            self.p21 = None
            self.p22 = None
            
            # Create actions 
            self.act_intersection= QAction(QIcon(":/plugins/cadtools/icons/pointandline.png"),  "Intersection Point",  self.iface.mainWindow())
            self.act_s2s= QAction(QIcon(":/plugins/cadtools/icons/select2lines.png"),  "Select 2 Line Segments",  self.iface.mainWindow())
            self.act_s2s.setCheckable(True)            
            
            # Connect to signals for button behaviour
            QObject.connect(self.act_s2s,  SIGNAL("triggered()"),  self.s2s)
            QObject.connect(self.act_intersection,  SIGNAL("triggered()"),  self.intersection) 
            QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)
            
            # Add actions to the toolbar
            toolBar.addAction(self.act_s2s)
            toolBar.addAction(self.act_intersection)
            #toolBar.addSeparator()
            
            # Get the tool
            self.tool = SegmentFinderTool(self.canvas)
         
        # Select 2 Line Segments
        def s2s(self):
            mc = self.canvas
            layer = mc.currentLayer()

            # Set SegmentFinderTool as current tool
            mc.setMapTool(self.tool)
            self.act_s2s.setChecked(True)        
                    
            #Connect to the SegmentFinderTool
            QObject.connect(self.tool, SIGNAL("segmentsFound(PyQt_PyObject)"), self.storeSegmentPoints)
            
        def storeSegmentPoints(self,  result):
            self.p11 = result[0]
            self.p12 = result[1]
            self.p21 = result[2]
            self.p22 = result[3]
            #QMessageBox.information(None,  "Cancel",  str(self.p11.toString()))

        def intersection(self):
            if self.p11 == None or self.p12 == None or self.p21 == None or self.p22 == None:
                QMessageBox.information(None,  "Cancel",  "Not enough line segments selected.")
            else:
                p = QgsPoint()
                p = LineIntersection.intersectionPoint(self.p11,  self.p12,  self.p21,  self.p22)
                
                g = None
                g = LineIntersection.intersectionLine(self.p11,  self.p12,  self.p21,  self.p22)
                
                if p <> None and g <> None:
                    cadutils.addGeometryToCadLayer(QgsGeometry.fromPoint(p))
                    cadutils.addGeometryToCadLayer(g)                    
                    self.canvas.refresh()

                self.unsetTool()
                self.deactivate()
                
                self.p11 = None
                self.p12 = None
                self.p21 = None
                self.p22 = None    
                
                                
        def intersect_line(self):
            if self.p11 == None or self.p12 == None or self.p21 == None or self.p22 == None:
                QMessageBox.information(None,  "Cancel",  "Not enough line segments selected.")
            else:
                g = None
                g = LineIntersection.intersectionLine(self.p11,  self.p12,  self.p21,  self.p22)
                if g <> None:
                    cadutils.addGeometryToCadLayer(g)
                    self.canvas.refresh()
                    
                self.unsetTool()
                self.deactivate()                    
                                    
                self.p11 = None
                self.p12 = None
                self.p21 = None
                self.p22 = None   
                    
        def unsetTool(self):
            mc = self.canvas
            mc.unsetMapTool(self.tool)                                                                    
                
        def deactivate(self):
            self.p11 = None
            self.p12 = None
            self.p21 = None
            self.p22 = None
            
            #uncheck the button/menu and get rid off the SFtool signal
            self.act_s2s.setChecked(False)
            QObject.disconnect(self.tool, SIGNAL("segmentsFound(PyQt_PyObject)"), self.storeSegmentPoints)                  
