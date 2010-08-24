# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import math

def addGeometryToCadLayer(g):
    pointName = "CadLayer Points"
    lineName = "CadLayer Lines"
    polygonName = "CadLayer Polygons"
        
    type = g.type()
        
    # Points
    if type == 0:
        theName = pointName
        theType = "Point"
    elif type ==1:
        theName = lineName
        theType = "LineString"
    elif type == 2:
        theName = polygonName
        theType = "Polygon"
    else:
        return
    
    if getCadLayerByName(theName) == None:
        vl = QgsVectorLayer(theType, theName, "memory")
        pr = vl.dataProvider()
        feat = QgsFeature()
        feat.setGeometry(g)
        pr.addFeatures([feat])
        vl.updateExtents()
        QgsMapLayerRegistry().instance().addMapLayer(vl, True)
    else:
        layer = getCadLayerByName(theName) 
        pr = layer.dataProvider()
        feat = QgsFeature()
        feat.setGeometry(g)
        pr.addFeatures([feat])
        layer.updateExtents()

def getCadLayerByName(cadname):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.name() == cadname:
            if layer.isValid():
                return layer
            else:
                return None        

def azimuth(p1,  p2):
    dx = p2.x()-p1.x()
    dy = p2.y()-p1.y()
    
    if dx == 0 and dy ==0:
        return None
    
    if dy == 0:
        if dx > 0:
            return math.pi / 2
        else:
            return 3 * math.pi / 2
    
    if dx == 0:
        if p1.y() < p2.y():
            return 0
        else:
            return math.pi

    if dx > 0 and dy > 0:
        return math.atan(dx/dy)
    elif dx > 0 and dy < 0:
        return math.atan(dx/dy) + math.pi
    elif dx < 0 and dy < 0:
        return math.atan(dx/dy) + math.pi
    else:
        return math.atan(dx/dy) + 2*math.pi        
    
def distance(p1, p2):
    return ( (p1.x()-p2.x())**2 + (p1.y()-p2.y())**2 )**0.5

# At the moment only simple LineStrings are supported
def helmert2d(geom, dX, dY, angle, scale):
    
    if geom.type() == 1:
        coordsTransformed = []
        
        coords = geom.asPolyline()
        for i in coords:
            x = dX + scale*math.cos(angle)*i.x() - scale*math.sin(angle)*i.y()
            y = dY + scale*math.sin(angle)*i.x() + scale*math.cos(angle)*i.y()
            coordsTransformed.append( QgsPoint(x,y) )
    else: 
        return None
    
    if len(coordsTransformed) > 1:
        g = QgsGeometry.fromPolyline(coordsTransformed)
        return g
    else:
        return None        
   
   
# Rotates a geometry.
# (c) Stefan Ziegler
def rotate(geom,  point,  angle):
    
    if angle == 0 or angle == 2 * math.pi or angle == -2 * math.pi:
        return geom
    
    type = geom.wkbType()
    
    if type == 1:
        p0 = geom.asPoint()
        p1 = QgsPoint(p0.x() - point.x(),  p0.y() - point.y())
        p2 = rotatePoint(p1,  angle)
        p3 = QgsPoint(point.x() + p2.x(),  point.y() + p2.y())
        return QgsGeometry().fromPoint(p3)
        
    elif type == 2:
        coords = []
        for i in geom.asPolyline():
            p1 = QgsPoint(i.x() - point.x(),  i.y() - point.y())
            p2 = rotatePoint(p1,  angle)
            p3 = QgsPoint(point.x() + p2.x(),  point.y() + p2.y())
            coords.append(p3)
        return QgsGeometry().fromPolyline(coords)

    elif type == 3:
        coords = []
        ring = []
        for i in geom.asPolygon():
            for k in i: 
                p1 = QgsPoint(k.x() - point.x(),  k.y() - point.y())
                p2 = rotatePoint(p1,  angle)
                p3 = QgsPoint(point.x() + p2.x(),  point.y() + p2.y())
                ring.append(p3)
            coords .append(ring)
            ring = []
        return QgsGeometry().fromPolygon(coords)
            
    elif type == 4:
        coords = []
        for i in geom.asMultiPoint():
            p1 = QgsPoint(i.x() - point.x(),  i.y() - point.y())
            p2 = rotatePoint(p1,  angle)
            p3 = QgsPoint(point.x() + p2.x(),  point.y() + p2.y())
            coords.append(p3)
        return QgsGeometry().fromMultiPoint(coords)
        
    elif type == 5:
        coords = []
        singleline = [] 
        for i in geom.asMultiPolyline():
            for j in i:
                p1 = QgsPoint(j.x() - point.x(),  j.y() - point.y())
                p2 = rotatePoint(p1,  angle)
                p3 = QgsPoint(point.x() + p2.x(),  point.y() + p2.y())
                singleline.append(p3)
            coords.append(singleline)
            singleline = []
        return QgsGeometry().fromMultiPolyline(coords)
        
    elif type == 6:
        coords = []
        ring = []
        for i in geom.asMultiPolygon():
            for j in i:
                for k in j:
                    p1 = QgsPoint(k.x() - point.x(),  k.y() - point.y())
                    p2 = rotatePoint(p1,  angle)
                    p3 = QgsPoint(point.x() + p2.x(),  point.y() + p2.y())
                    ring.append(p3)                    
                coords.append(ring)
                ring = []
        return QgsGeometry().fromMultiPolygon([coords])
        
    else:
        QMessageBox.information(None, 'Information', str("Vector type is not supported."))   
        return None


# Rotates a single point (centre 0/0).
# (c) Stefan Ziegler
def rotatePoint(point,  angle):
    x = math.cos(angle)*point.x() - math.sin(angle)*point.y()
    y = math.sin(angle)*point.x() + math.cos(angle)*point.y()
    return QgsPoint(x,  y)
