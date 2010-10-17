# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import webbrowser, os
import os.path, sys

# Set up current path, so that we know where to look for modules
currentPath = os.path.dirname( __file__ )
sys.path.append( os.path.abspath( os.path.dirname( __file__) + '/tools' ) )

#Import own tools
from lineintersectiontool import LineIntersectionTool
from arcintersectiontool import ArcIntersectionTool
from orthogonaldigitizertool import OrthogonalDigitizerTool
from orthoelementsonsegmenttool import OrthoElementsOnSegmentTool
from rectangularpointstool import RectangularPointsTool
from showazimuthtool import ShowAzimuthTool
from rotateobjecttool import RotateObjectTool
from parallellinetool import ParallelLineTool
from circulararctool import CircularArcTool
from modifycirculararctool import ModifyCircularArcTool
from orthogonaltraversetool import OrthogonalTraverseTool
from circulararcdigitizertool import CircularArcDigitizerTool
from cadtoolsaboutgui import CadToolsAboutGui
from cadtoolssettingsgui import CadToolsSettingsGui


class CadTools:

    def __init__(self, iface):
    # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

    def initGui(self):
        # Add toolbar 
        self.toolBar = self.iface.addToolBar("CAD-Tools")
        self.toolBar.setObjectName("CAD-Tools")
        
        self.menu = QMenu()
        self.menu.setTitle( QCoreApplication.translate( "CadTools","&CadTools" ) )
        self.cadtools_help = QAction( QCoreApplication.translate("CadTools", "Help" ), self.iface.mainWindow() )
        self.cadtools_about = QAction( QCoreApplication.translate("CadTools", "About" ), self.iface.mainWindow() )
        self.cadtools_settings = QAction( QCoreApplication.translate("CadTools", "Settings" ), self.iface.mainWindow() )
        
        # this is just a test.....
##        self.cadtools_dock = QAction( QCoreApplication.translate("CadTools","dock test"), self.iface.mainWindow() )
##        self.menu.addActions( [self.cadtools_help, self.cadtools_about, self.cadtools_dock] )
  
        self.menu.addActions( [self.cadtools_help, self.cadtools_about,  self.cadtools_settings] )

        menu_bar = self.iface.mainWindow().menuBar()
        actions = menu_bar.actions()
        lastAction = actions[ len( actions ) - 1 ]
        menu_bar.insertMenu( lastAction, self.menu )

        QObject.connect( self.cadtools_about, SIGNAL("triggered()"), self.doAbout )   
        QObject.connect( self.cadtools_help, SIGNAL("triggered()"), self.doHelp )    
        QObject.connect( self.cadtools_settings, SIGNAL("triggered()"), self.doSettings )    

        # this is just a test......... 
##        QObject.connect( self.cadtools_dock, SIGNAL("triggered()"), self.doTheDock )    
        
        # Get the tools
        self.lineintersector = LineIntersectionTool(self.iface,  self.toolBar)
        self.arcintersector = ArcIntersectionTool(self.iface,  self.toolBar)
        self.orthoelements = OrthoElementsOnSegmentTool(self.iface, self.toolBar)
        self.rectangularpoints = RectangularPointsTool(self.iface, self.toolBar)       
        self.orthogonaltraverse = OrthogonalTraverseTool(self.iface, self.toolBar)        
        self.showazimuth = ShowAzimuthTool(self.iface,  self.toolBar)         
        self.rotateobject = RotateObjectTool(self.iface,  self.toolBar)
        self.parallelline = ParallelLineTool(self.iface,  self.toolBar)
        self.circulararc = CircularArcTool(self.iface,  self.toolBar)
        self.modifycirculararc = ModifyCircularArcTool(self.iface,  self.toolBar)
        self.circulararcdigitizer = CircularArcDigitizerTool(self.iface,  self.toolBar)        
        self.orthogonaldigitizer = OrthogonalDigitizerTool(self.iface,  self.toolBar, self.menu)
        
        
##    def doTheDock(self):
##        self.dockWidget=CadConsole(self)
##        self.dockWidget.initGui()
##        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget)
        
        
    def doAbout(self):
        d = CadToolsAboutGui(self.iface.mainWindow())
        d.show()

    def doHelp(self):
        webbrowser.open(currentPath + "/help/cadtools_help.html")
        
    def doSettings(self):
        settings = CadToolsSettingsGui(self.iface.mainWindow())
        settings.show()

    def unload(self):
        # remove toolbar and menubar
        del self.toolBar
        del self.menu
        
        
