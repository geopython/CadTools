# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from cadconsole import *

# Initialize Qt resources from file resources.py
from cadtools import resources

#Import own classes and tools
#from segmentfindertool import SegmentFinderTool
#from lineintersection import LineIntersection
from orthogonaldigitizer import OrthogonalDigitizer

class OrthogonalDigitizerTool():
    
        def __init__(self, iface,  toolBar, menu):
            # Save reference to the QGIS interface
            self.iface = iface
            self.canvas = self.iface.mapCanvas()
            mc = self.canvas
            self.tool = None
            
            # Create actions 
            self.act_console = QAction(QIcon(":/plugins/cadtools/icons/cadconsole2.png"), QCoreApplication.translate("CadTools","Cad Console"), self.iface.mainWindow() )
            self.act_ortho = QAction(QIcon(":/plugins/cadtools/icons/ortho.png"),  "Capture Orthogonal Lines/Polygons",  self.iface.mainWindow())
            self.act_ortho.setEnabled(False)
            self.act_ortho.setCheckable(True)            
            
            # Connect to signals for button behaviour
            QObject.connect(self.act_ortho,  SIGNAL("triggered()"),  self.orthodigitize)
            QObject.connect(self.iface, SIGNAL("currentLayerChanged(QgsMapLayer*)"), self.toggle)
            QObject.connect(mc, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)         
            QObject.connect( self.act_console, SIGNAL("triggered()"), self.showCadConsole )    
            
            # Add actions to the toolbar
            toolBar.addSeparator()
            toolBar.addAction(self.act_ortho)
            
            # Add the console to the menu and to the toolbar
            toolBar.addSeparator()
            toolBar.addAction(self.act_console)
#            menu.addAction( self.act_console )
            
            # Get the tool
            self.tool = OrthogonalDigitizer(self.canvas)
            
        # Show the CAD console
        def showCadConsole(self):
            if self.tool == None:
                self.tool = OrthogonalDigitizer(self.canvas)
                
            self.dockWidget=CadConsole(self, self.tool)
            self.dockWidget.initGui()
            self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget)
            
         
        # Select 2 Line Segments
        def orthodigitize(self):
            mc = self.canvas
            layer = mc.currentLayer()
            
            # Set OrthogonalTool as current tool
            mc.setMapTool(self.tool)
            self.act_ortho.setChecked(True)    
                
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
                            self.act_ortho.setEnabled(True)
                            QObject.connect(layer,SIGNAL("editingStopped()"),self.toggle)
                            QObject.disconnect(layer,SIGNAL("editingStarted()"),self.toggle)
                        else:
                            self.act_ortho.setEnabled(False)
                            QObject.connect(layer,SIGNAL("editingStarted()"),self.toggle)
                            QObject.disconnect(layer,SIGNAL("editingStopped()"),self.toggle)                   
                
        def deactivate(self):
            #uncheck the button/menu and get rid off the SFtool signal
            self.act_ortho.setChecked(False)
            #QObject.disconnect(self.tool, SIGNAL("segmentsFound(PyQt_PyObject)"), self.storeSegmentPoints)                  
