# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# Initialize Qt resources from file resources.py
from cadtools import resources

#Import own classes and tools
from horizontalverticaldigitizer import HorizontalVerticalDigitizer

class HorizontalVerticalDigitizerTool():
    
        def __init__(self, iface,  toolBar):
            self.iface = iface
            self.canvas = self.iface.mapCanvas()
            mc = self.canvas
            self.tool = None
            
            self.act_horivert = QAction(QIcon(":/plugins/cadtools/icons/hvdigitizer.png"), QCoreApplication.translate("ctools", "Capture Vertical/Horizontal Lines/Polygons"),  self.iface.mainWindow())
            self.act_horivert.setEnabled(False)
            self.act_horivert.setCheckable(True)            
            
            self.act_horivert.triggered.connect(self.hvdigitize)
            self.iface.currentLayerChanged.connect(self.toggle)
            mc.mapToolSet.connect(self.deactivate)
            
            toolBar.addSeparator()
            toolBar.addAction(self.act_horivert)

            self.tool = HorizontalVerticalDigitizer(self.canvas)
            

        def hvdigitize(self):
            mc = self.canvas
            layer = mc.currentLayer()
            
            mc.setMapTool(self.tool)
            self.act_horivert.setChecked(True)    


        def toggle(self):
            mc = self.canvas
            layer = mc.currentLayer()
            
            #Decide whether the plugin button/menu is enabled or disabled
            if layer <> None:
                # Only for vector layers
                type = layer.type()
                if type == 0:
                    gtype = layer.geometryType()
                    # Doesn't make sense for Points
                    if gtype <> 0:
                        if layer.isEditable():
                            self.act_horivert.setEnabled(True)
                            layer.editingStopped.connect(self.toggle)
                            try:
                                layer.editingStarted.disconnect(self.toggle)
                            except TypeError:
                                pass
                        else:
                            self.act_horivert.setEnabled(False)
                            layer.editingStarted.connect(self.toggle)
                            try:
                                layer.editingStopped.disconnect(self.toggle)
                            except TypeError:
                                pass


        def deactivate(self):
            self.act_horivert.setChecked(False)
            # try:
            #     self.tool.segmentsFound.disconnect(self.storeSegmentPoints)
            # except TypeError:
            #     pass
