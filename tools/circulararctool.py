# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources

## Import own classes and tools.
from threearcpointsfindertool import ThreeArcPointsFinderTool
from circulararcgui import CircularArcGui
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
            self.action_selectthreepoints = QAction(QIcon(":/plugins/cadtools/icons/select3points.png"),  "Select three points",  self.iface.mainWindow())
            self.action_circulararc = QAction(QIcon(":/plugins/cadtools/icons/circulararc.png"),  "Create circular arc",  self.iface.mainWindow())
            self.action_selectthreepoints.setCheckable(True)      
      
            # Connect to signals for button behaviour      
            QObject.connect(self.action_selectthreepoints,  SIGNAL("triggered()"),  self.selectThreePoints)
            QObject.connect(self.action_circulararc,   SIGNAL("triggered()"),  self.showDialog)
            QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)

            toolBar.addSeparator()
            toolBar.addAction(self.action_selectthreepoints)
            toolBar.addAction(self.action_circulararc)
                        
            
        def selectThreePoints(self):
            print "************************** 99999"
            
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


        def showDialog(self):
            print "************************ 8888"
            if self.p1 == None or self.p2 == None or self.p3 == None:
                QMessageBox.information(None,  "Cancel",  "Not enough points selected.")
            else:
                
                flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
                self.ctrl = CircularArcGui(self.iface.mainWindow(),  flags)
                self.ctrl.initGui()
                self.ctrl.show()
                
                QObject.connect(self.ctrl, SIGNAL("okClicked(QString, double)"), self.createCircularArc)
                QObject.connect( self.ctrl, SIGNAL("unsetTool()"), self.unsetTool )
                
                
                # connect the signals
#                QObject.connect(self.ctrl, SIGNAL("distancesFromPoints(double, double)"), self.calculateArcIntersection)
#                QObject.connect(self.ctrl, SIGNAL("closeArcIntersectionGui()"), self.deactivate)
#                QObject.connect(self.ctrl, SIGNAL("unsetTool()"), self.unsetTool)


        def createCircularArc(self, method,  value):
            print "***************************"
            print value;
            
            g = CircularArc.getInterpolatedArc(self.p1,  self.p2,  self.p3,  method,  value)
            cadutils.addGeometryToCadLayer(g)     
            self.canvas.refresh()
            
            

        def unsetTool(self):
            print "***************** unset tool"  
            self.p1 = None
            self.p2 = None
            self.p3 = None          
            mc = self.canvas
            mc.unsetMapTool(self.tool)      
            self.action_selectthreepoints.setChecked(False)       
      

        def deactivate(self):
            print "***************** deactivate"            
            self.action_selectthreepoints.setChecked(False)   
            

