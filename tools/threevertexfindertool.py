# -*- coding: latin1 -*-


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

# Vertex Finder Tool class
class ThreeVertexFinderTool(QgsMapTool):
  def __init__(self, canvas):
    QgsMapTool.__init__(self,canvas)
    self.canvas = canvas
    # number of marked vertex
    self.count = 0
    # 2 markers and vertex points
    self.m1 = None #QgsVertexMarker(self.canvas)
    self.m2 = None #QgsVertexMarker(self.canvas)
    self.m3 = None
    self.p1 = QgsPoint()
    self.p2 = QgsPoint()
    self.p3 = QgsPoint()
    #our own fancy cursor
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
                                  
 
    
 
  def canvasPressEvent(self,event):
    pass
  
  def canvasMoveEvent(self,event):
    pass
  
  def canvasReleaseEvent(self,event):
    #Get the click
    x = event.pos().x()
    y = event.pos().y()
    
    layer = self.canvas.currentLayer()
    
    if layer <> None:
      #the clicked point is our starting point
      startingPoint = QPoint(x,y)
      
      #we need a snapper, so we use the MapCanvas snapper   
      snapper = QgsMapCanvasSnapper(self.canvas)
      
      # Try first the current layer, if we don't find anything try
      # the background layers.
      (retval,result) = snapper.snapToCurrentLayer (startingPoint,QgsSnapper.SnapToVertex)
      if result == []:
          (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
      if result <> []:
          
        #mark the vertex 
        if self.count == 0:
            self.p1.setX( result[0].snappedVertex.x() )  
            self.p1.setY( result[0].snappedVertex.y() )  
            
            self.m1 = QgsVertexMarker(self.canvas)
            self.m1.setIconType(3)
            self.m1.setColor(QColor(255,0,0))
            self.m1.setIconSize(12)
            self.m1.setPenWidth (3)            
            self.m1.setCenter(self.p1)

            self.count = self.count + 1
            
        elif self.count == 1:
            self.p2.setX( result[0].snappedVertex.x() )  
            self.p2.setY( result[0].snappedVertex.y() )  

            self.m2 = QgsVertexMarker(self.canvas)
            self.m2.setIconType(1)
            self.m2.setColor(QColor(0,0,255))
            self.m2.setIconSize(12)
            self.m2.setPenWidth (3)            
            self.m2.setCenter(self.p2)

            self.count = self.count + 1
            
        elif self.count == 2:
            self.p3.setX( result[0].snappedVertex.x() )  
            self.p3.setY( result[0].snappedVertex.y() )  

            self.m3 = QgsVertexMarker(self.canvas)
            self.m3.setIconType(1)
            self.m3.setColor(QColor(0,0,255))
            self.m3.setIconSize(12)
            self.m3.setPenWidth (3)            
            self.m3.setCenter(self.p3)

            self.count = self.count + 1            
            
            self.emit(SIGNAL("vertexFound(PyQt_PyObject)"), [self.p1, self.p2,  self.p3])

        elif self.count % 3 == 0:
            
            #QMessageBox.information(None,  "Cancel",  str(self.m1))
            
            self.p1.setX( result[0].snappedVertex.x() )
            self.p1.setY( result[0].snappedVertex.y()  )
            self.m1.setCenter(self.p1)
            
            self.count = self.count + 1  
            
            ## Falls jetzt wirklich jemand öfters klickt als Integer zulässt....
            if self.count > 300:
                self.count = 4

            self.emit(SIGNAL("vertexFound(PyQt_PyObject)"), [self.p1, self.p2,  self.p3])


        elif self.count > 3 and self.count % 3 != 0:
            
            self.p2.setX( self.p3.x() )
            self.p2.setY( self.p3.y()  )
            self.m2.setCenter(self.p2)            
            
            self.p3.setX( result[0].snappedVertex.x() )
            self.p3.setY( result[0].snappedVertex.y()  )
            self.m3.setCenter(self.p3)
            
            self.count = self.count + 1              
            
            self.emit(SIGNAL("vertexFound(PyQt_PyObject)"), [self.p1, self.p2,  self.p3])

    else:
        #warn about missing snapping tolerance if appropriate
        self.showSettingsWarning()
            
  def showSettingsWarning(self):
    #get the setting for displaySnapWarning
    settings = QSettings()
    settingsLabel = "/UI/displaySnapWarning"
    displaySnapWarning = settings.value(settingsLabel).toBool()
    
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
    self.canvas.scene().removeItem(self.m2)   
    self.canvas.scene().removeItem(self.m3)   
    self.m1 = None 
    self.m2 = None 
    self.m3 = None
    self.count = 0 
    pass

  def isZoomTool(self):
    return False
  
  def isTransient(self):
    return False
    
  def isEditTool(self):
    return True
