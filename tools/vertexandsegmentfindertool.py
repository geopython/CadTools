# -*- coding: latin1 -*-


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

# Vertex Finder Tool class
class VertexAndSegmentFinderTool(QgsMapTool):
  def __init__(self, canvas):
    QgsMapTool.__init__(self,canvas)
    self.canvas=canvas
    # number of marked vertex
    self.count = 0
    # A marker for the vertex point and a rubberband for the linesegment
    self.m1 = None #QgsVertexMarker(self.canvas)
    self.p1 = QgsPoint()
    self.rb1 = QgsRubberBand(self.canvas,  False)
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
      
      #we snap to the current layer (we don't have exclude points and use the tolerances from the qgis properties)
      #(retval,result) = snapper.snapToCurrentLayer (startingPoint,QgsSnapper.SnapToVertex)
    
      # First we just want vertex, no segments.
      if self.count == 0:
        (retval,result) = snapper.snapToCurrentLayer(startingPoint,QgsSnapper.SnapToVertex)
      else:
       (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
                       
      #so if we have found a vertex
      if result <> []:
        color = QColor(255,0,0)
          
        #mark the vertex 
        if self.count == 0:
            self.canvas.scene().removeItem(self.m1)            
            
            self.p1.setX( result[0].snappedVertex.x() )  
            self.p1.setY( result[0].snappedVertex.y() )  
            
            self.m1 = QgsVertexMarker(self.canvas)
            self.m1.setIconType(1)
            self.m1.setColor(color)
            self.m1.setIconSize(10)
            self.m1.setPenWidth (2)            
            self.m1.setCenter(self.p1)

            self.count = self.count + 1
        elif self.count == 1:
            self.rb1.reset()
            self.rb1.setColor(color)
            self.rb1.setWidth(2)
            
            #print str(result[0].beforeVertex.toString())
            #print str(result[0].afterVertex.toString())
            
            #QMessageBox.information(None,  "Cancel",  str(result[0].beforeVertexNr) + str(result[0].afterVertexNr))
            
            beforeVertexNr = result[0].beforeVertexNr
            afterVertexNr = result[0].afterVertexNr
            if afterVertexNr - beforeVertexNr == 1:
                self.rb1.addPoint(result[0].beforeVertex)
                self.rb1.addPoint(result[0].afterVertex)
                self.rb1.show()
            
                self.count = 0
        
                self.emit(SIGNAL("vertexAndSegmentFound(PyQt_PyObject)"), [self.p1, self.rb1.getPoint(0,0), self.rb1.getPoint(0,2)])
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
    # Remove the marked vertex
    self.canvas.scene().removeItem(self.m1)
    self.m1 = None 
    # Reset the rubberband
    self.rb1.reset()
    self.count = 0 
    pass

  def isZoomTool(self):
    return False
  
  def isTransient(self):
    return False
    
  def isEditTool(self):
    return True
