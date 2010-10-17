# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import math

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
        self.featId = None
        self.movingVertex = "arc"
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

        x = event.pos().x()
        y = event.pos().y()
        
        self.layer = self.canvas.currentLayer()
        
        startingPoint = QPoint(x,y)
        snapper = QgsMapCanvasSnapper(self.canvas)
        (retval, result) = snapper.snapToCurrentLayer (startingPoint, QgsSnapper.SnapToVertex)
        
        if result <> []:

            self.clicked = True
            
            feat = QgsFeature()
            self.featId = result[0].snappedAtGeometry
            self.layer.featureAtId(self.featId,  feat,  True,  False)
            
            wkbType = feat.geometry().wkbType()
            
            if wkbType == 2:
                line = feat.geometry().asPolyline()
            elif wkbType == 5:
                line = feat.geometry().asMultiPolyline()
                line = line[0]
            else: 
                QMessageBox.information(None,  "Modify Circular Arc",  "Unsupported geometry type.")
                return
            
            ## Get the three arc points. 
            ## a) the snapped vertex is the first point of the linestring
            ## b) it is the last one
            ## c) neither first nor last one
            if result[0].beforeVertexNr == -1 and result[0].snappedVertexNr == 0:
                self.ptStart = result[0].snappedVertex
                self.ptArc = line[int(len(line)/2)]
                self.ptEnd = line[len(line)-1]
                self.movingVertex = "start"
            
            elif result[0].afterVertexNr == -1 and result[0].snappedVertexNr == ( len(line) - 1 ):
                self.ptStart = line[0]
                self.ptArc = line[int(len(line)/2)]
                self.ptEnd = result[0].snappedVertex
                self.movingVertex = "end"                
                
            else:
                self.ptStart = line[0]
                self.ptArc = result[0].snappedVertex
                self.ptEnd = line[len(line)-1]
                self.movingVertex = "arc"

            self.rb2 = self.createRubberBand( QColor(0, 0, 255) )
            

    def canvasMoveEvent(self,event):
        if self.featId != None and self.clicked == True:
            ## Try to snap to active or background layer first.
            x = event.pos().x()
            y = event.pos().y()
            startingPoint = QPoint(x,y)            
            snapper = QgsMapCanvasSnapper(self.canvas)
            (retval,result) = snapper.snapToCurrentLayer (startingPoint,QgsSnapper.SnapToVertex)   
            if result <> []:
                newPoint = result[0].snappedVertex
            else:
                (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
                if result <> []:
                    newPoint = result[0].snappedVertex
                else:
                    newPoint = self.toLayerCoordinates( self.layer, event.pos() )

            ## Create the new geometry (circular arc) for the moving rubberband and 
            ## the final feature.
            settings = QSettings("CatAIS","cadtools")
            value = settings.value("arcs/rubberangle",  5)
            if self.movingVertex == "arc":
                g = CircularArc.getInterpolatedArc(self.ptStart,  newPoint,  self.ptEnd,  "angle",   value.toDouble()[0])                
            elif self.movingVertex == "start":
                g = CircularArc.getInterpolatedArc(newPoint,  self.ptArc,  self.ptEnd,  "angle",   value.toDouble()[0])
            elif self.movingVertex == "end":
                g = CircularArc.getInterpolatedArc(self.ptStart,  self.ptArc,  newPoint,  "angle",   value.toDouble()[0])                
                
            self.rb2.setToGeometry( g, self.layer );
            
#            print str(self.ptStart.toString())
#            print str(newPoint.toString())
#            print str(self.ptEnd.toString())
            
        pass
  
  
    def canvasReleaseEvent(self,event):
        if self.rb2 <> None:
            ## Reset the rubberband.
            self.rb2.reset()
            self.rb2 = None
            
            ## What happens to newPoint???? Even as self.newPoint it 
            ## does not work....
            ## We just snap again....
            x = event.pos().x()
            y = event.pos().y()
            startingPoint = QPoint(x,y)            
            snapper = QgsMapCanvasSnapper(self.canvas)
            (retval,result) = snapper.snapToCurrentLayer (startingPoint,QgsSnapper.SnapToVertex)   
            if result <> []:
                newPoint = result[0].snappedVertex
            else:
                (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
                if result <> []:
                    newPoint = result[0].snappedVertex
                else:
                    newPoint = self.toLayerCoordinates( self.layer, event.pos() )
        
            ## Modify the feature.
            settings = QSettings("CatAIS","cadtools")
            method = settings.value("arcs/featuremethod",  "pitch")
            if method == "pitch":
                value = settings.value("arcs/featurepitch",  2)
            else:
                value = settings.value("arcs/featureangle",  1)
            if self.movingVertex == "arc":
                g = CircularArc.getInterpolatedArc(self.ptStart,  newPoint,  self.ptEnd,  method,   value.toDouble()[0])                
            elif self.movingVertex == "start":
                g = CircularArc.getInterpolatedArc(newPoint,  self.ptArc,  self.ptEnd,  method, value.toDouble()[0])
            elif self.movingVertex == "end":
                g = CircularArc.getInterpolatedArc(self.ptStart,  self.ptArc,  newPoint,  method, value.toDouble()[0])    
                
            ## On the Fly reprojection of the geometry (only if needed)
            layerEPSG = self.layer.srs().epsg()
            projectEPSG = self.canvas.mapRenderer().destinationSrs().epsg()
            if layerEPSG != projectEPSG:
                layerSRS = self.layer.srs()
                projectSRS = self.canvas.mapRenderer().destinationSrs()
                coordtrans = QgsCoordinateTransform(layerSRS,  projectSRS)
                g.transform(coordtrans)
        
            self.layer.beginEditCommand("Geometry modified.")
            self.layer.changeGeometry(self.featId,  g)
            self.layer.endEditCommand()
            self.layer.setModified(True,  True)
            self.layer.reload()
            self.canvas.refresh()
            
        ## Reset some stuff.
        self.clicked = False
        self.featId = None
        
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
        if self.rb2 <> None:
            self.rb2.reset()
        pass


    def isZoomTool(self):
        return False


    def isTransient(self):
        return False
    
    
    def isEditTool(self):
        return True
