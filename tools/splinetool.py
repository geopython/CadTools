# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# Initialize Qt resources from file resources.py
#from cadtools import resources

#Import own classes and tools
from spline import Spline

class SplineTool():
    
        def __init__(self, iface,  toolBar):
            # Save reference to the QGIS interface
            self.iface = iface
            self.canvas = self.iface.mapCanvas()
            mc = self.canvas
            self.tool = None
            
            # Create actions 
            self.action_spline = QAction(QIcon(":/plugins/cadtools/icons/spline.png"), QCoreApplication.translate("ctools", "Create Spline Lines/Polygons"),  self.iface.mainWindow())
            self.action_spline.setEnabled(False)
            self.action_spline.setCheckable(True)            
            
            # Connect to signals for button behaviour
            self.action_spline.triggered.connect(self.digitize)
            self.iface.currentLayerChanged.connect(self.toggle)
            mc.mapToolSet.connect(self.deactivate)
            
            # Add actions to the toolbar
            toolBar.addSeparator()
            toolBar.addAction(self.action_spline)
                        
            # Get the tool
            self.tool = Spline(self.iface)
         
        def digitize(self):
            mc = self.canvas
            layer = mc.currentLayer()
            
            mc.setMapTool(self.tool)
            self.action_spline.setChecked(True)    
                
                
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
                            self.action_spline.setEnabled(True)
                            layer.editingStopped.connect(self.toggle)
                            try:
                                layer.editingStarted.disconnect(self.toggle)
                            except TypeError:
                                pass
                        else:
                            self.action_spline.setEnabled(False)
                            layer.editingStarted.connect(self.toggle)
                            try:
                                layer.editingStopped.disconnect(self.toggle)
                            except TypeError:
                                pass
                
                
        def deactivate(self):
            self.action_spline.setChecked(False)
