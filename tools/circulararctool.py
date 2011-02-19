# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from cadtools import resources

## Import own classes and tools.
from threearcpointsfindertool import ThreeArcPointsFinderTool
from circulararc import CircularArc
import cadutils

class CircularArcTool:
    
        def __init__(self, iface,  toolBar):
            # Save reference to the QGIS interface
            self.iface = iface
            self.canvas = self.iface.mapCanvas()
            
            # Points for arc
            self.p1 = None
            self.p2 = None
            self.p3 = None
            
            # Create actions 
            self.action_selectthreepoints = QAction(QIcon(":/plugins/cadtools/icons/select3points.png"),  "Select Three Points",  self.iface.mainWindow())
            self.action_circulararc = QAction(QIcon(":/plugins/cadtools/icons/circulararc.png"),  "Create Circular Arc",  self.iface.mainWindow())
            self.action_selectthreepoints.setCheckable(True)      
      
            # Connect to signals for button behaviour      
            QObject.connect(self.action_selectthreepoints,  SIGNAL("triggered()"),  self.selectThreePoints)
            QObject.connect(self.action_circulararc,   SIGNAL("triggered()"),  self.createCircularArc)
            QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)

            toolBar.addSeparator()
            toolBar.addAction(self.action_selectthreepoints)
            toolBar.addAction(self.action_circulararc)
                        
            
        def selectThreePoints(self):
            mc = self.canvas
            layer = mc.currentLayer()
            
            self.tool = ThreeArcPointsFinderTool(self.canvas)           
            mc.setMapTool(self.tool)
            
            self.action_selectthreepoints.setChecked(True)                    
            
            #Connect to the FinderTool
            QObject.connect(self.tool, SIGNAL("arcPointsFound(PyQt_PyObject)"), self.storeArcPoints)


        def storeArcPoints(self,  result):
            self.p1 = result[0]
            self.p2 = result[1]
            self.p3 = result[2]


        def createCircularArc(self):
            settings = QSettings("CatAIS","cadtools")
            method = settings.value("arcs/featuremethod",  "pitch")
            if method == "pitch":
                value = settings.value("arcs/featurepitch",  2)
            else:
                value = settings.value("arcs/featureangle",  1)

            if self.p1 == None or self.p2 == None or self.p3 == None:
                QMessageBox.information(None,  "Cancel",  "Not enough points selected.")
            else:
                g = CircularArc.getInterpolatedArc(self.p1,  self.p2,  self.p3,  method.toString(),  value.toDouble()[0])
                cadutils.addGeometryToCadLayer(g)     
                self.canvas.refresh()
                
                self.unsetTool()
        

        def unsetTool(self):
            print "***************** unset tool"  
            self.p1 = None
            self.p2 = None
            self.p3 = None          
            mc = self.canvas
            mc.unsetMapTool(self.tool)      
            self.action_selectthreepoints.setChecked(False)       
      

        def deactivate(self):
            print "***************** deactivate circulararctool"            
            self.action_selectthreepoints.setChecked(False)   
            

