# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from cadtools import resources

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
            self.action_modifycirculararc.setCheckable(True) 
            self.action_modifycirculararc.setEnabled(False) 
      
            # Connect to signals for button behaviour      
            QObject.connect(self.action_modifycirculararc,  SIGNAL("triggered()"),  self.modifycirculararc)
            QObject.connect(self.iface, SIGNAL("currentLayerChanged(QgsMapLayer*)"), self.toggle)
            QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)

            toolBar.addSeparator()
            toolBar.addAction(self.action_modifycirculararc)

            mc = self.canvas
            self.tool = ArcFinderTool(mc)        
 
            
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
#            self.tool = ArcFinderTool(mc)           
            mc.setMapTool(self.tool)
            self.action_modifycirculararc.setChecked(True) 
            

        def toggle(self):
            mc = self.canvas
            layer = mc.currentLayer()
            
            ## Decide whether the plugin button/menu is enabled or disabled.
            if layer <> None:
                ## Only for vector layers.
                type = layer.type()
                if type == 0:
                    gtype = layer.geometryType()
                    ## Does only work for Polylines and MultiPolylines.
                    if gtype == 1:
                        if layer.isEditable():
                            self.action_modifycirculararc.setEnabled(True) 
                            QObject.connect(layer,SIGNAL("editingStopped()"),self.toggle)
                            QObject.disconnect(layer,SIGNAL("editingStarted()"),self.toggle)
                        else:
                            self.action_modifycirculararc.setEnabled(False) 
                            QObject.connect(layer,SIGNAL("editingStarted()"),self.toggle)
                            QObject.disconnect(layer,SIGNAL("editingStopped()"),self.toggle)        


        def unsetTool(self):
            print "***************** unset tool modifycirculararctool"  
#            self.p1 = None
#            self.p2 = None
#            self.p3 = None          
            mc = self.canvas
            mc.unsetMapTool(self.tool)      
            self.action_modifycirculararc.setChecked(False)       
 
 
        def deactivate(self):
            print "***************** deactivate modifycirculararctool"            
            self.action_modifycirculararc.setChecked(False)   
            

