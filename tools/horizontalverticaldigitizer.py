# -*- coding: latin1 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import math, time

from lineintersection import LineIntersection

# Orthogonal Tool class
class HorizontalVerticalDigitizer(QgsMapTool):
  def __init__(self, canvas):
    QgsMapTool.__init__(self,canvas)
    self.canvas=canvas
    self.rb = QgsRubberBand(self.canvas,  True)
    self.mCtrl = False
    self.pp1 = QgsPoint()
    self.offset = 0.00001
    
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
 
 
  def canvasPressEvent(self,event):
    color = QColor(255,0,0)
    self.rb.setColor(color) 
    self.rb.setWidth(1)      
    
    x = event.pos().x()
    y = event.pos().y()
    
    if event.button() == Qt.LeftButton:
        
        ## This is the same as in the canvasMoveEvent.
        ## Is there an easier way??? Or more logical way?
        startingPoint = QPoint(x,y)
        snapper = QgsMapCanvasSnapper(self.canvas)
        
        (retval,result) = snapper.snapToCurrentLayer (startingPoint,QgsSnapper.SnapToVertex)   
        if result <> []:
            point = result[0].snappedVertex
        else:
            (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
            if result <> []:
                point = result[0].snappedVertex
            else:
                point = self.canvas.getCoordinateTransform().toMapCoordinates( event.pos().x(), event.pos().y() );

        if self.mCtrl == True:
            self.rb.movePoint(self.pp1) 
            
        self.rb.addPoint(point)
        
    else:
        self.createFeature()
    
    
  def createFeature(self):
     
    layer = self.canvas.currentLayer() 
    provider = layer.dataProvider()
    f = QgsFeature()

    if self.isPolygon == True:
        if self.mCtrl == True:        
            # the last segment 
            pn = self.rb.getPoint(0,  self.rb.numberOfVertices()-2)
            pm = self.rb.getPoint(0,  self.rb.numberOfVertices()-1)
            
            p1 = self.rb.getPoint(0, 0)
            p2 = self.rb.getPoint(0, 1)

            # but we need a line segment that is orthogonal to the last segment
            # der letzte Punkt ist der Aufpunkt
            # der Richtungsvektor ist der Vektor, der rechwinklig zum Differenzvektor pn-pm liegt (-> x/y vertauschen)
            d = ( (pn.x()-pm.x())**2 + (pn.y()-pm.y())**2 )**0.5
            xp = p1.x() + (p1.y()-p2.y()) 
            yp = p1.y() - (p1.x()-p2.x())  
            pp = QgsPoint(xp,  yp)
        
            p0 = LineIntersection.intersectionPoint(pn, pm, p1, pp)
#            self.rb.movePoint(self.rb.numberOfVertices()-1, p0, 0)

            # ODER:
            dx = math.fabs(pn.x() - pm.x())
            # Use a small value as tolerance.
            if dx < self.offset:
                self.rb.movePoint(self.rb.numberOfVertices()-1, QgsPoint(pm.x(), p1.y()), 0)
            else:
                self.rb.movePoint(self.rb.numberOfVertices()-1, QgsPoint(p1.x(), pm.y()), 0)
        
    coords = []
    [coords.append(self.rb.getPoint(0, i)) for i in range(self.rb.numberOfVertices())]
    
    ## On the Fly reprojection.
    layerEPSG = layer.srs().epsg()
    projectEPSG = self.canvas.mapRenderer().destinationSrs().epsg()
    
    if layerEPSG != projectEPSG:
        coords_tmp = coords[:]
        coords = []
        for point in coords_tmp:
            transformedPoint = self.canvas.mapRenderer().mapToLayerCoordinates(layer, point);
            coords.append(transformedPoint)
          
    # Add geometry to feature.
    if self.isPolygon == True:
        g = QgsGeometry().fromPolygon([coords])
    else:
        g = QgsGeometry().fromPolyline(coords)
        
    if g is None:
        pass
    else:
        f.setGeometry(g)
            
        # Add attributefields to feature.
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
        

  def azimuth(self,  p1,  p2):
    dx = p2.x()-p1.x()
    dy = p2.y()-p1.y()
    
    # division by zero
    if dy == 0:
        if dx > 0:
            return math.pi / 2
        else:
            return 3 * math.pi / 2
    
    # four cases
    if dx > 0 and dy > 0:
        return math.atan(dx/dy)
    elif dx > 0 and dy < 0:
        return math.atan(dx/dy) + math.pi
    elif dx < 0 and dy < 0:
        return math.atan(dx/dy) + math.pi
    else:
        return math.atan(dx/dy) + 2*math.pi
     

  def horizontalverticalPnt(self, p1, p2):
    mAzi = self.azimuth(p1, p2)
    
    if mAzi > 1.75*math.pi or mAzi <= 0.25*math.pi:
        xp = p1.x()
        yp = p2.y()
        return QgsPoint(xp,  yp)        
    elif mAzi > 0.25*math.pi and mAzi <= 0.75*math.pi:
        xp = p2.x()
        yp = p1.y()
#        xp = p1.x() + 10000
        return QgsPoint(xp,  yp)                
    elif mAzi > 0.75*math.pi and mAzi <= 1.25*math.pi:
        xp = p1.x()
        yp = p2.y()
        return QgsPoint(xp,  yp)                
    elif mAzi > 1.25*math.pi and mAzi <= 1.75*math.pi:
        xp = p2.x()
        yp = p1.y()
        return QgsPoint(xp,  yp)                
    else:
        xp = p1.x()
        yp = p2.y()    
        return QgsPoint(xp,  yp)        

  
  def canvasMoveEvent(self,event):
    x = event.pos().x()
    y = event.pos().y()
    
    startingPoint = QPoint(x,y)
    snapper = QgsMapCanvasSnapper(self.canvas)
        
    # Try to get a point from the foreground snapper. 
    # If we don't get one we try the backround snapper and
    # at last we do not snap.
    (retval,result) = snapper.snapToCurrentLayer (startingPoint,QgsSnapper.SnapToVertex)   
    if result <> []:
        point = result[0].snappedVertex
    else:
        (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
        if result <> []:
            point = result[0].snappedVertex
        else:
            point = self.canvas.getCoordinateTransform().toMapCoordinates( event.pos().x(), event.pos().y() );
        
    if self.mCtrl == True:
        count = self.rb.numberOfVertices() 
        if count > 0:
            p1 = self.rb.getPoint(0, count-2)
            self.pp1 = self.horizontalverticalPnt(p1, point)
            
            # The rubberband is not drawn if the 2nd point is horzontal
            # or vertical. So we save the original point add some offset 
            # and when adding a vertex point we move back to the
            # original point.
            pp2 = QgsPoint(self.pp1.x()+self.offset, self.pp1.y()+self.offset)
            self.rb.movePoint(pp2)
    else:
        self.rb.movePoint(point)
    

  def canvasReleaseEvent(self,event):
    pass 


  def showSettingsWarning(self):
    pass


  def activate(self):
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
