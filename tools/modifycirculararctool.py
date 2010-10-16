# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources

## Import own classes and tools.
from arcfindertool import ArcFinderTool
#from circulararcgui import CircularArcGui
#from circulararc import CircularArc
import cadutils

class ModifyCircularArcTool:
    
        def __init__(self, iface,  toolBar):
            # Save reference to the QGIS interface
            self.iface = iface
            self.canvas = self.iface.mapCanvas()
            
            # Points for arc
            self.p1 = None
            self.p2 = None
            self.p3 = None
            
            # Create actions 
            self.action_modifycirculararc = QAction(QIcon(":/plugins/cadtools/icons/modifycirculararc.png"),  "Modify Circular Arc",  self.iface.mainWindow())
#            self.action_circulararc = QAction(QIcon(":/plugins/cadtools/icons/circulararc.png"),  "Create circular arc",  self.iface.mainWindow())
            self.action_modifycirculararc.setCheckable(True)      
      
            # Connect to signals for button behaviour      
            QObject.connect(self.action_modifycirculararc,  SIGNAL("triggered()"),  self.modifycirculararc)
#            QObject.connect(self.action_circulararc,   SIGNAL("triggered()"),  self.createCircularArc)
#            QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)

            toolBar.addSeparator()
            toolBar.addAction(self.action_modifycirculararc)
#            toolBar.addAction(self.action_circulararc)
                        
            
        def modifycirculararc(self):
            
            ## It works only for linestring layers.
            vlayer = self.canvas.currentLayer()
            if vlayer == None:
                self.action_modifycirculararc.setChecked(False) 
                return
            
            self.type = vlayer.geometryType()
            if self.type <> 1:
                QMessageBox.information(None,  "Modify Circular Arc",  "Unsupported geometry type.")
                self.action_modifycirculararc.setChecked(False)   
                return
            
            ## Set the selection/finder tool.
            mc = self.canvas
            self.tool = ArcFinderTool(mc)           
            mc.setMapTool(self.tool)
            

            
            
            
            print "**************************33 modifycirculararc"
            
#        def selectThreePoints(self):
#            mc = self.canvas
#            layer = mc.currentLayer()
#            
#            self.tool = ThreeArcPointsFinderTool(self.canvas)           
#            mc.setMapTool(self.tool)
#            
#            self.action_selectthreepoints.setChecked(True)                    
#            
#            #Connect to the FinderTool
#            QObject.connect(self.tool, SIGNAL("arcPointsFound(PyQt_PyObject)"), self.storeArcPoints)
#
#
#        def storeArcPoints(self,  result):
#            self.p1 = result[0]
#            self.p2 = result[1]
#            self.p3 = result[2]
#
#
#        def showDialog(self):
#            if self.p1 == None or self.p2 == None or self.p3 == None:
#                QMessageBox.information(None,  "Cancel",  "Not enough points selected.")
#            else:
#                
#                flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint  # QgisGui.ModalDialogFlags
#                self.ctrl = CircularArcGui(self.iface.mainWindow(),  flags)
#                self.ctrl.initGui()
#                self.ctrl.show()
#                
#                QObject.connect(self.ctrl, SIGNAL("okClicked(QString, double)"), self.createCircularArc)
#                QObject.connect( self.ctrl, SIGNAL("unsetTool()"), self.unsetTool )
#                
#                
#                # connect the signals
##                QObject.connect(self.ctrl, SIGNAL("distancesFromPoints(double, double)"), self.calculateArcIntersection)
##                QObject.connect(self.ctrl, SIGNAL("closeArcIntersectionGui()"), self.deactivate)
##                QObject.connect(self.ctrl, SIGNAL("unsetTool()"), self.unsetTool)
#
#
#        def createCircularArc(self):
#            settings = QSettings("CatAIS","cadtools")
#            method = settings.value("arcs/featuremethod",  "pitch")
#            if method == "pitch":
#                value = settings.value("arcs/featurepitch",  2)
#            else:
#                value = settings.value("arcs/featureangle",  1)
#
#            g = CircularArc.getInterpolatedArc(self.p1,  self.p2,  self.p3,  method.toString(),  value.toDouble()[0])
#            cadutils.addGeometryToCadLayer(g)     
#            self.canvas.refresh()
#        
#
#        def unsetTool(self):
#            print "***************** unset tool"  
#            self.p1 = None
#            self.p2 = None
#            self.p3 = None          
#            mc = self.canvas
#            mc.unsetMapTool(self.tool)      
#            self.action_selectthreepoints.setChecked(False)       
#      
#
#        def deactivate(self):
#            print "***************** deactivate"            
#            self.action_selectthreepoints.setChecked(False)   
            

