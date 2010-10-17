# -*- coding: latin1 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import math

from circulararc import CircularArc


class CircularArcDigitizer(QgsMapTool):
    def __init__(self, canvas):
        QgsMapTool.__init__(self,canvas)
        self.canvas=canvas
        self.rb = QgsRubberBand(self.canvas,  True)
        self.mCtrl = False
        self.count = 0
        
        self.ptStart = None
        self.ptArc = None
        self.ptEnd = None

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
                                  
 

    def setOrtho(self, toggle):
        self.mCtrl = toggle
    
    def setLength(self,  length):
        self.length = length

    def keyPressEvent(self,  event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = True


    def keyReleaseEvent(self,  event):
        if event.key() == Qt.Key_Control:
            self.mCtrl = False
            self.count = 0
 
 
    def canvasPressEvent(self,event):
        color = QColor(255,0,0)
        self.rb.setColor(color) 
        self.rb.setWidth(1)      
        
        x = event.pos().x()
        y = event.pos().y()
        
        if event.button() == Qt.LeftButton:
            
            ## This is the same as in the canvasMoveEvent.
            ## Is there an easier way??? Or  more logical way?
            startingPoint = QPoint(x,y)
            snapper = QgsMapCanvasSnapper(self.canvas)
            
            (retval,result) = snapper.snapToCurrentLayer (startingPoint, QgsSnapper.SnapToVertex)   
            if result <> []:
                point = result[0].snappedVertex
            else:
                (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
                if result <> []:
                    point = result[0].snappedVertex
                else:
                    point = self.canvas.getCoordinateTransform().toMapCoordinates( event.pos().x(), event.pos().y() );
            
            self.rb.addPoint(point)
            
            if self.mCtrl == True:
                if self.count == 0:
                    self.ptStart = QgsPoint( point.x(),  point.y() )
                    print str(self.ptStart.toString())
                    print "******************** NUmmer EINS...."
                elif self.count == 1:
                    self.ptArc = QgsPoint( point.x(),  point.y() )
                    print "******************** NUmmer ZWEI...."
                elif self.count == 2:
                    
                    print "******************** NUmmer drei...."
                    print str(self.ptStart.toString())
                    
                    self.ptEnd = QgsPoint( point.x(),  point.y() )
                    self.count = -1
                    
                    ## Remove the last three points 
                    ## and create the circular arc.
                    self.rb.removeLastPoint( )
                    self.rb.removeLastPoint( )
                    self.rb.removeLastPoint( )
                    
                    settings = QSettings("CatAIS","cadtools")
                    method = settings.value("arcs/featuremethod",  "pitch")
                    if method == "pitch":
                        value = settings.value("arcs/featurepitch",  2)
                    else:
                        value = settings.value("arcs/featureangle",  1)

                    g = CircularArc.getInterpolatedArc(self.ptStart,  self.ptArc,  self.ptEnd,  method.toString(),  value.toDouble()[0])
                    ptList = g.asPolyline()
                    
                    ## Add the segmentation points to the rubberband.
                    for i in ptList:
                        self.rb.addPoint(i)
                    
                    self.mCtrl == False
                self.count = self.count + 1
            
        else:
            self.createFeature()
    
    def createFeature(self):
        layer = self.canvas.currentLayer() 
        provider = layer.dataProvider()
        f = QgsFeature()
            
        coords = []
        [coords.append(self.rb.getPoint(0, i)) for i in range(self.rb.numberOfVertices())]
        
        ## On the Fly reprojection.
        layerEPSG = layer.srs().epsg()
        projectEPSG = self.canvas.mapRenderer().destinationSrs().epsg()
        
        if layerEPSG != projectEPSG:
            coords_tmp = coords[:]
            coords = []
            for point in coords_tmp:
                transformedPoint = self.canvas.mapRenderer().mapToLayerCoordinates( layer, point );
                coords.append(transformedPoint)
              
        ## Add geometry to feature.
        if self.isPolygon == True:
            g = QgsGeometry().fromPolygon([coords])
        else:
            g = QgsGeometry().fromPolyline(coords)
        f.setGeometry(g)
            
        ## Add attributefields to feature.
        fields = layer.pendingFields()
        for i in fields:
            f.addAttribute(i,  provider.defaultValue(i))
                
        layer.beginEditCommand("Feature added")
        layer.addFeature(f)
        layer.endEditCommand()
            
        # reset rubberband and refresh the canvas
        if self.type == 1:
            self.isPolygon = False
        else:
            self.isPolygon = True
            
        self.rb.reset(self.isPolygon)
        self.canvas.refresh()
        
  
    def canvasMoveEvent(self,event):
        x = event.pos().x()
        y = event.pos().y()
        
        startingPoint = QPoint(x,y)
        snapper = QgsMapCanvasSnapper(self.canvas)
            
        ## Try to get a point from the foreground snapper. 
        ## If we don't get one we try the backround snapper and
        ## at last we do not snap.
        (retval,result) = snapper.snapToCurrentLayer (startingPoint,QgsSnapper.SnapToVertex)   
        if result <> []:
            point = result[0].snappedVertex
        else:
            (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
            if result <> []:
                point = result[0].snappedVertex
            else:
                point = self.canvas.getCoordinateTransform().toMapCoordinates( event.pos().x(), event.pos().y() );
            

        self.rb.movePoint(point)
    

    def canvasReleaseEvent(self,event):
        pass 


    def showSettingsWarning(self):
        pass


    def activate(self):
        ## Set our new cursor.
        self.canvas.setCursor(self.cursor)
        
        ## Check wether Geometry is a Line or a Polygon
        mc = self.canvas
        layer = mc.currentLayer()
        self.type = layer.geometryType()
        self.isPolygon = True
        if self.type == 1:
            self.isPolygon = False
        else:
            self.isPolygon = True
        self.rb.reset(self.isPolygon)


    def deactivate(self):
        self.rb.reset(True)
        self.count = 0
        pass


    def isZoomTool(self):
        return False
  
  
    def isTransient(self):
        return False
    
    
    def isEditTool(self):
        return True
