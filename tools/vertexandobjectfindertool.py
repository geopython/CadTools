# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

class VertexAndObjectFinderTool(QgsMapTool):

    vertexAndObjectFound = pyqtSignal(object)

    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.count = 0
        self.rb = None
        self.m1 = None 
        self.p1 = QgsPoint()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #FFFFFF",
                                      "                ",
                                      "       +.+      ",
                                      "      ++.++     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " ++.    .    .++",
                                      " ... ...+... ...",
                                      " ++.    .    .++",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "   ++.     .+   ",
                                      "    ++.....+    ",
                                      "      ++.++     ",
                                      "       +.+      "]))
                                      
 
    
 
    def canvasPressEvent(self, event):

        ## First we need to select the object.
        if self.count % 2 == 0:

            vlayer = self.canvas.currentLayer()
            if vlayer is None:
                return
            
            self.type = vlayer.geometryType()
            self.isPolygon = True
            if self.type == 1:
                self.isPolygon = False
            else:
                self.isPolygon = True
            
            if self.rb is not None:
                if self.isPolygon:
                    self.rb.reset(QGis.Polygon)
                else:
                    self.rb.reset()

            layerCoords = self.toLayerCoordinates( vlayer, event.pos() )
            searchRadius = QgsTolerance.vertexSearchRadius( vlayer, self.canvas.mapRenderer() )


            pointGeometry = QgsGeometry.fromPoint( layerCoords )
            if pointGeometry is None:
              return

            try:
                minDistance = float('inf')
            except ValueError:
                minDistance = 1e100000
            
#            minDistance = 1e100000

            self.cf = QgsFeature()
            for f in vlayer.getFeatures():
                if f.geometry() is not None:
                    currentDistance = pointGeometry.distance( f.geometry() )
                    if currentDistance < minDistance:
                        minDistance = currentDistance
                        self.cf.setGeometry(f.geometry())
            try:
                if minDistance == float('inf'):
                    return
            except ValueError:
                if minDistance == 1e100000:
                    return
                    
#            if minDistance == 1e100000:
#                return


            self.rb = self.createRubberBand(self.isPolygon)
            self.rb.setToGeometry( self.cf.geometry(), vlayer )

            self.count += 1

            if self.count > 1:
                self.vertexAndObjectFound.emit([self.p1, self.cf,  self.m1,  self.rb])
                
        ## Then we have to select a vertex point (=centre of rotation).
        elif self.count % 2 == 1:
        
            x = event.pos().x()
            y = event.pos().y()
            
            layer = self.canvas.currentLayer()
            
            if layer is not None:
              startingPoint = QPoint(x,y)
              snapper = QgsMapCanvasSnapper(self.canvas)
              (retval,result) = snapper.snapToCurrentLayer (startingPoint,QgsSnapper.SnapToVertex)
                               
              if result == []:
                  (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
              if result <> []:
                self.p1.setX( result[0].snappedVertex.x() )  
                self.p1.setY( result[0].snappedVertex.y() )  
                
                if self.m1 is None:
                    self.m1 = QgsVertexMarker(self.canvas)
                    self.m1.setIconType(3)
                    self.m1.setColor(QColor(255,0,0))
                    self.m1.setIconSize(12)
                    self.m1.setPenWidth (3)            
                self.m1.setCenter(self.p1)

                self.count += 1

                if self.count > 1:
                    self.vertexAndObjectFound.emit([self.p1, self.cf,  self.m1,  self.rb])
                    

    def canvasMoveEvent(self,event):
        pass
  
  
    def canvasReleaseEvent(self,event):
        pass


    def createRubberBand( self, isPolygon ):
        if isPolygon:
            rb = QgsRubberBand( self.canvas, QGis.Polygon )
        else:
            rb = QgsRubberBand( self.canvas )
        color = QColor(255,0,0,100)
        rb.setColor(color) 
        rb.setWidth(2)      
        rb.show()
        return rb

            
    def showSettingsWarning(self):
        #get the setting for displaySnapWarning
        settings = QSettings()
        settingsLabel = "/UI/displaySnapWarning"
        displaySnapWarning = bool(settings.value(settingsLabel))
        
        #only show the warning if the setting is true
        if displaySnapWarning:    
          m = QgsMessageViewer()
          m.setWindowTitle("Snap tolerance")
          m.setCheckBoxText("Don't show this message again")
          m.setCheckBoxVisible(True)
          m.setCheckBoxQSettingsLabel(settingsLabel)
          m.setMessageAsHtml( "<p>Could not snap vertex.</p><p>Have you set the tolerance in Settings > Project Properties > General?</p>")
          m.showMessage()
    
    def activate(self):
        self.canvas.setCursor(self.cursor)
  
    def deactivate(self):
        self.canvas.scene().removeItem(self.m1)
        self.m1 = None
        if self.rb is not None:
            self.rb.reset()
        self.count = 0 
        pass

    def isZoomTool(self):
        return False
  
    def isTransient(self):
        return False
    
    def isEditTool(self):
        return True
