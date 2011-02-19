# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# Initialize Qt resources from file resources.py
from cadtools import resources

#Import own classes and tools
from circulararcdigitizer import CircularArcDigitizer

class CircularArcDigitizerTool():
    
        def __init__(self, iface,  toolBar):
            # Save reference to the QGIS interface
            self.iface = iface
            self.canvas = self.iface.mapCanvas()
            mc = self.canvas
            self.tool = None
            
            # Create actions 
            self.action_capturecirculararc = QAction(QIcon(":/plugins/cadtools/icons/capturecirculararc.png"),  "Capture Circular Arc Lines/Polygons",  self.iface.mainWindow())
            self.action_capturecirculararc.setEnabled(False)
            self.action_capturecirculararc.setCheckable(True)            
            
            # Connect to signals for button behaviour
            QObject.connect(self.action_capturecirculararc,  SIGNAL("triggered()"),  self.orthodigitize)
            QObject.connect(self.iface, SIGNAL("currentLayerChanged(QgsMapLayer*)"), self.toggle)
            QObject.connect(mc, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)         
            
            # Add actions to the toolbar
            toolBar.addSeparator()
            toolBar.addAction(self.action_capturecirculararc)
                        
            # Get the tool
            self.tool = CircularArcDigitizer(self.canvas)
                        
         
        def orthodigitize(self):
            mc = self.canvas
            layer = mc.currentLayer()
            
            # Set OrthogonalTool as current tool
            mc.setMapTool(self.tool)
            self.action_capturecirculararc.setChecked(True)    
                
                
        def toggle(self):
            mc = self.canvas
            layer = mc.currentLayer()
            
            #Decide whether the plugin button/menu is enabled or disabled.
            if layer <> None:
                # Only for vector layers.
                type = layer.type()
                if type == 0:
                    gtype = layer.geometryType()
                    # Doesn't make sense for points.
                    if gtype <> 0:
                        if layer.isEditable():
                            self.action_capturecirculararc.setEnabled(True)
                            QObject.connect(layer,SIGNAL("editingStopped()"),self.toggle)
                            QObject.disconnect(layer,SIGNAL("editingStarted()"),self.toggle)
                        else:
                            self.action_capturecirculararc.setEnabled(False)
                            QObject.connect(layer,SIGNAL("editingStarted()"),self.toggle)
                            QObject.disconnect(layer,SIGNAL("editingStopped()"),self.toggle)                   
                
                
        def deactivate(self):
            self.action_capturecirculararc.setChecked(False)
            #QObject.disconnect(self.tool, SIGNAL("segmentsFound(PyQt_PyObject)"), self.storeSegmentPoints)                  
