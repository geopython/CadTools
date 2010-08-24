# -*- coding: latin1 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import math

from lineintersection import LineIntersection

# Orthogonal Tool class
class OrthogonalDigitizer(QgsMapTool):
  def __init__(self, canvas):
    QgsMapTool.__init__(self,canvas)
    self.canvas=canvas
    self.rb = QgsRubberBand(self.canvas,  True)
    self.mCtrl = False
    self.length = -1
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
        ## Is there an easier way??? Or  more logical way?
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

        self.rb.addPoint(point)
    else:
        #print "right button"
        self.createFeature()
    
  def createFeature(self):
     
    layer = self.canvas.currentLayer() 
    provider = layer.dataProvider()
    f = QgsFeature()

    if self.isPolygon == True:
        if self.mCtrl == True:
            # we will move the first point to close the polygon square... (square??)
        
            # the last segment 
            pn = self.rb.getPoint(0,  self.rb.numberOfVertices()-2)
            pm = self.rb.getPoint(0,  self.rb.numberOfVertices()-1)
        
            # but we need a line segment that ist orthogonal to the last segment
            # der letzte Punkt ist der Aufpunkt
            # der Richtungsvektor ist der Vektor, der rechwinklig zum Differenzvektor pn-pm liegt (-> x/y vertauschen)
            d = ( (pn.x()-pm.x())**2 + (pn.y()-pm.y())**2 )**0.5
            xp = pm.x() + (pm.y()-pn.y()) 
            yp = pm.y() - (pm.x()-pn.x())  
            pp = QgsPoint(xp,  yp)
        
            p0 = LineIntersection.intersectionPoint(self.rb.getPoint(0,  0),  self.rb.getPoint(0,  1),  pm,  pp)
            self.rb.movePoint(0,  p0,  0)
        
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
        

  # azimuth of two points  
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
     
    
  def orthoPnt(self,  p1,  p2,  p3):
    mAzi1 = self.azimuth(p2,  p1)
    mAzi2 = self.azimuth(p2,  p3)
    mAngle = mAzi1-mAzi2
    
    # Könnte/müsste man nur einmal in der mousemoveevent machen, halt einfach als erstes.
    if self.length > 0:
        az = self.azimuth(p2,  p3);
        xn =  p2.x() + self.length*math.sin(az)
        yn =  p2.y() + self.length*math.cos(az)
        p3 = QgsPoint(xn, yn)

        
    d1 = ( (p1.x()-p2.x())**2 + (p1.y()-p2.y())**2 )**0.5
    d2 = ( (p3.x()-p2.x())**2 + (p3.y()-p2.y())**2 )**0.5    
    
    try:
        if mAngle >= 0.25*math.pi and mAngle <= 0.75*math.pi :
            #print "case 1"
            xp = p2.x() + d2*math.cos(mAngle-0.5*math.pi) * (p2.y()-p1.y()) / d1
            yp = p2.y() + d2*math.cos(mAngle-0.5*math.pi) * -(p2.x()-p1.x()) / d1 
            return QgsPoint(xp,  yp)
        elif mAngle <= -0.25*math.pi and mAngle >= -0.75*math.pi :
            #print "case 2"
            xp = p2.x() + d2*math.cos(mAngle-0.5*math.pi) * (p2.y()-p1.y()) / d1 
            yp = p2.y() + d2*math.cos(mAngle-0.5*math.pi) * -(p2.x()-p1.x()) / d1 
            return QgsPoint(xp,  yp)        
        elif mAngle >= 1.25*math.pi and mAngle <= 1.75*math.pi :
            #print "case 3"
            xp = p2.x() + d2*math.cos(mAngle-0.5*math.pi) * (p2.y()-p1.y()) / d1 
            yp = p2.y() + d2*math.cos(mAngle-0.5*math.pi) * -(p2.x()-p1.x()) / d1 
            return QgsPoint(xp,  yp)        
        elif mAngle <= -1.25*math.pi and mAngle >= -1.75*math.pi :
            #print "case 4"
            xp = p2.x() + d2*math.cos(mAngle-0.5*math.pi) * (p2.y()-p1.y()) / d1 
            yp = p2.y() + d2*math.cos(mAngle-0.5*math.pi) * -(p2.x()-p1.x()) / d1 
            return QgsPoint(xp,  yp)     
        if mAngle > 0.75*math.pi or mAngle < -0.75*math.pi :
            #print "case 5"
            xp = p2.x() + d2*math.sin(mAngle-0.5*math.pi) * (p2.x()-p1.x()) / d1
            yp = p2.y() + d2*math.sin(mAngle-0.5*math.pi) * (p2.y()-p1.y()) / d1 
            return QgsPoint(xp,  yp)        
    except ZeroDivisionError:
        return p3     

    return p3


  def movePointPolar(self, azi, dist):
    
    count = self.rb.numberOfVertices()
    
    if count > 2:
        p1 = self.rb.getPoint(0, count-3)
        p2 = self.rb.getPoint(0, count-2)    

        angle = self.azimuth(p1,  p2)
        
        x = p2.x() + dist*math.sin(azi*math.pi/180 + angle)
        y = p2.y() + dist*math.cos(azi*math.pi/180 + angle)
        
        point = QgsPoint(x,y) 
        
        self.rb.movePoint(point)
        self.rb.addPoint(point)
    else:
        return False   
    
  def movePointOrthogonal(self, abscissa, ordinate):
    count = self.rb.numberOfVertices()
    if count > 2:
        # calculate polar elements
        if abscissa == 0:
            if ordinate > 0:
                self.movePointPolar(90, ordinate)
            elif ordinate < 0:
                self.movePointPolar(float(270), abs(ordinate))
        else:
            azi = math.atan(ordinate/abscissa)
            if ordinate < 0:
                azi = 2*math.pi - azi
            
            dist = (abscissa**2+ordinate**2)**0.5
            self.movePointPolar(azi*180/math.pi, dist)
    else:
        return False           
        
        
  def closePolygon(self):
    count = self.rb.numberOfVertices()
    if count > 2:
        p0 = self.rb.getPoint(0, 0)    
        self.rb.addPoint(p0)
        self.createFeature()
      

  def closeLine(self):
      self.closePolygon()    
  
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
        
    ## Orthogonal condition doesn't make sense with only one point.
    count = self.rb.numberOfVertices()
    
    if count > 2:    
        p1 = self.rb.getPoint(0, count-3)
        p2 = self.rb.getPoint(0, count-2)
        
        if self.mCtrl == True:
            ## This is the orthogonal projected point.
            pp = self.orthoPnt(p1,  p2,  point)
            self.rb.movePoint(pp)
        else:
            ## length condition
            if self.length > 0:
                az = self.azimuth(p2,  point);
                xn =  p2.x() + self.length*math.sin(az)
                yn =  p2.y() + self.length*math.cos(az)
                pn = QgsPoint(xn, yn)
                self.rb.movePoint(pn)
            else:
                self.rb.movePoint(point)
    
    ## Second vertex point.
    elif count == 2:
        p2 = self.rb.getPoint(0, count-2)        
        ## length condition
        if self.length > 0:
            az = self.azimuth(p2,  point);
            xn =  p2.x() + self.length*math.sin(az)
            yn =  p2.y() + self.length*math.cos(az)
            pn = QgsPoint(xn, yn)
            self.rb.movePoint(pn)
        else:
            self.rb.movePoint(point)
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
