# -*- coding: latin1 -*-


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

# Vertex Finder Tool class
class SegmentFinderTool(QgsMapTool):
  def __init__(self, canvas):
    QgsMapTool.__init__(self,canvas)
    self.canvas=canvas
    self.rb1 = QgsRubberBand(self.canvas,  False)
    self.rb2 = QgsRubberBand(self.canvas,  False)
    self.count = 0
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
      (retval,result) = snapper.snapToCurrentLayer (startingPoint,QgsSnapper.SnapToSegment)
                       
      #so if we have found a vertex
      if result <> []:

        # we like to mark the segment that is choosen, so we need a rubberband
        color = QColor(255,0,0)
        
        if self.count == 0:
            #QMessageBox.information(None,  "Cancel",  str("0"))
            self.rb1.setColor(color)
            self.rb1.setWidth(2)
    
            self.rb1.addPoint(result[0].beforeVertex)
            self.rb1.addPoint(result[0].afterVertex)
            self.rb1.show()

        if self.count == 1:
            self.rb2.reset()
            self.rb2.setColor(color)
            self.rb2.setWidth(2)
        
            self.rb2.addPoint(result[0].beforeVertex)
            self.rb2.addPoint(result[0].afterVertex)
            self.rb2.show()        
            
        if self.count == 2:
            self.rb1.reset()
            self.rb1.addPoint(self.rb2.getPoint(0, 0)) 
            if QGis.QGIS_VERSION_INT >= 10700:            
                self.rb1.addPoint(self.rb2.getPoint(0, 1)) 
            else:
                self.rb1.addPoint(self.rb2.getPoint(0, 2)) 
            self.rb1.show()
                        
            self.rb2.reset() 
            self.rb2.addPoint(result[0].beforeVertex) 
            self.rb2.addPoint(result[0].afterVertex)
            self.rb2.show()  
                        
            self.count =  1
            
        self.count = self.count + 1
        
        #QMessageBox.information(None,  "Cancel",  str(self.rb1.getPoint(0, 0)) + " - " + str(self.rb1.getPoint(0, 2)) + " - " + str(self.rb2.getPoint(0, 0)) + " - " + str(self.rb2.getPoint(0, 2)) )
        
        #tell the world about the segments  
        if self.count == 2:
            if QGis.QGIS_VERSION_INT >= 10700:
                self.emit(SIGNAL("segmentsFound(PyQt_PyObject)"), [self.rb1.getPoint(0, 0),  self.rb1.getPoint(0, 1),  self.rb2.getPoint(0, 0),  self.rb2.getPoint(0, 1)])
            else:
                self.emit(SIGNAL("segmentsFound(PyQt_PyObject)"), [self.rb1.getPoint(0, 0),  self.rb1.getPoint(0, 2),  self.rb2.getPoint(0, 0),  self.rb2.getPoint(0, 2)])
         
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
      m.setMessageAsHtml( "<p>Could not snap segment.</p><p>Have you set the tolerance in Settings > Project Properties > General?</p>")
      m.showMessage()
    
  def activate(self):
    self.canvas.setCursor(self.cursor)
  
  def deactivate(self):
    self.rb1.reset()
    self.rb2.reset()
    self.count = 0
    pass

  def isZoomTool(self):
    return False
  
  def isTransient(self):
    return False
    
  def isEditTool(self):
    return True
