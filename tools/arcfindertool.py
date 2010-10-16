# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from circulararc import CircularArc
import cadutils

class ArcFinderTool(QgsMapTool):
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.count = 0
        self.rb1 = None
        self.rb2 = None
        self.m1 = None 
        self.p1 = QgsPoint()
        self.ptStart = None
        self.ptArc = None
        self.ptEnd = None
        self.clicked = False
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
    
        if self.rb1 != None:
            self.rb1.reset(False)

        x = event.pos().x()
        y = event.pos().y()
        
        self.layer = self.canvas.currentLayer()
        
        startingPoint = QPoint(x,y)
        snapper = QgsMapCanvasSnapper(self.canvas)
        (retval, result) = snapper.snapToCurrentLayer (startingPoint, QgsSnapper.SnapToVertex)
        
        if result <> []:
            print str(result[0].snappedVertex.toString())
            print str(result[0].snappedAtGeometry)
            
            self.clicked = True
            
            feat = QgsFeature()
            self.layer.featureAtId(result[0].snappedAtGeometry,  feat,  True,  False)
            
            wkbType = feat.geometry().wkbType()
            print "*************"
            print str(feat.geometry().wkbType())
            
            if wkbType == 2:
                line = feat.geometry().asPolyline()
            elif wkbType == 5:
                line = feat.geometry().asMultiPolyline()
                line = line[0]
            else: 
                QMessageBox.information(None,  "Modify Circular Arc",  "Unsupported geometry type.")
                return
            
            ## The three arc points are the first and the last one
            ## from the linestring and the snapped vertex.
            ## TODO: falls erster oder letzter geklickt.......
            self.ptStart = line[0]
            self.ptArc = result[0].snappedVertex
            self.ptEnd = line[len(line)-1]
            
            # Unterscheidung hier, speicher und dann beim moveevent unterscheiden
            
            print str(self.ptStart.toString())
            print str(self.ptArc.toString())
            print str(self.ptEnd.toString())

            self.rb1 = self.createRubberBand( QColor(255,0,0) );
            self.rb1.setToGeometry( feat.geometry(), self.layer );
            
            self.rb2 = self.createRubberBand( QColor(0, 0, 255) )
            

    def canvasMoveEvent(self,event):
        if self.rb1 != None and self.clicked == True:
            print "************************mouse bewegen aber nur mit rubberband...."
            
            newPoint = self.toLayerCoordinates( self.layer, event.pos() )
            
            ## Calculate the new circular arc.
            settings = QSettings("CatAIS","cadtools")
            value = settings.value("arcs/featureangle",  5)

            g = CircularArc.getInterpolatedArc(self.ptStart,  newPoint,  self.ptEnd,  "angle",   value.toDouble()[0])
        
#            
#            cadutils.addGeometryToCadLayer(g)     
#            self.canvas.refresh()
#            
            self.rb2.setToGeometry( g, self.layer );
            
            
        
        pass
  
  
    def canvasReleaseEvent(self,event):
        print "************************* release...."
        self.clicked = False
        print str(self.clicked)
        
        self.rb2.reset()        
        pass


    def createRubberBand( self,  color ):
        rb = QgsRubberBand( self.canvas, False );
        rb.setColor(color) 
        rb.setWidth(2)      
        rb.show();
        return rb

            
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
        self.m1 = None
        if self.rb1 <> None:
            self.rb1.reset()
        if self.rb2 <> None:
            self.rb2.reset()
        pass


    def isZoomTool(self):
        return False


    def isTransient(self):
        return False
    
    def isEditTool(self):
        return True
