# -*- coding: latin1 -*-
"""
/***************************************************************************
    Digitize spline, based on CircularArcDigitizer (Stefan Ziegler)
    and Generalizer plugin (Piotr Pociask) which is based on GRASS v.generalize
                              -------------------
        begin                : February 2014
        copyright            : (C) 2014 by Radim Blazek
        email                : radim.blazek@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import math

#from circulararc import CircularArc
import cadutils


class Spline(QgsMapTool):
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        QgsMapTool.__init__(self,self.canvas)
        self.rb = QgsRubberBand(self.canvas,  QGis.Polygon)
        self.points = [] # digitized, not yet interpolated points

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
        color = QColor(255,0,0,100)
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
            
            #self.rb.addPoint(point)
            
            self.points.append(point)
            points = self.interpolate ( self.points )
            self.setRubberBandPoints(points )

        else:
            if len( self.points ) >= 2:
                self.createFeature()

            self.resetPoints()
            self.resetRubberBand()
            self.canvas.refresh()
            
    def resetPoints(self):
        self.points = []
    
    # Create feature from digitized points, i.e. without the last moving point 
    # where right click happend. This the same way how core QGIS Add Feature works.
    def createFeature(self):
        layer = self.canvas.currentLayer() 
        provider = layer.dataProvider()
        fields = layer.pendingFields()
        f = QgsFeature(fields)
            
        coords = []
        coords = self.interpolate ( self.points )
        
        ## On the Fly reprojection.
        layerEPSG = cadutils.authidToCrs(layer.crs().authid())
        projectEPSG = cadutils.authidToCrs(self.canvas.mapRenderer().destinationCrs().authid())
        
        if layerEPSG != projectEPSG:
            coords_tmp = coords[:]
            coords = []
            for point in coords_tmp:
                transformedPoint = self.canvas.mapRenderer().mapToLayerCoordinates( layer, point )
                coords.append(transformedPoint)
              
        ## Add geometry to feature.
        if self.isPolygon == True:
            g = QgsGeometry().fromPolygon([coords])
        else:
            g = QgsGeometry().fromPolyline(coords)
        f.setGeometry(g)
            
        ## Add attributefields to feature.
        for field in fields.toList():
            ix = fields.indexFromName(field.name())
            f[field.name()] = provider.defaultValue(ix)

        layer.beginEditCommand("Feature added")
        
        settings = QSettings()
        disable_attributes = settings.value( "/qgis/digitizing/disable_enter_attribute_values_dialog", False, type=bool)
        if disable_attributes:
            layer.addFeature(f)
            layer.endEditCommand()
        else:
            dlg = self.iface.getFeatureForm(layer, f)
            if dlg.exec_():
                layer.addFeature(f)
                layer.endEditCommand()
            else:
                layer.destroyEditCommand()
            
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
            
        points = list( self.points )
        points.append( point )
        points = self.interpolate ( points )
        self.setRubberBandPoints(points )
    
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
        self.isPolygon = False
        if self.type == QGis.Polygon:
            self.isPolygon = True

    def resetRubberBand(self):
        self.rb.reset( self.type )

    def setRubberBandPoints(self,points):
        self.resetRubberBand()
        for point in points:
            update = point is points[-1]
            self.rb.addPoint( point, update )

    def deactivate(self):
        self.rb.reset(QGis.Polygon)
        self.count = 0
        pass

    def isZoomTool(self):
        return False
  
  
    def isTransient(self):
        return False
    
    
    def isEditTool(self):
        return True

    # from given points create interpolated spline
    def interpolate(self, points):
        # always read settings to get changed value immediately
        settings = QSettings("CatAIS","cadtools")
        self.tolerance = float( settings.value("spline/tolerance", 1. ) )
        self.tightness = float( settings.value("spline/tightness", 0.5 ) )
        points = self.hermite( points, self.tolerance, self.tightness )
        return points

    # tolerance is maximum threshold for output line interpolation 
    def hermite(self, points, tolerance, tightness):
        npoints = len(points)
        if npoints < 3: return list(points) # return copy

        output = [] # output points

        # calculate tangents, first and last go in edge direction
        tangents = []
        tangents.append ( self.pointsTangentScaled( points[0], points[1], tightness ) )
        for i in range(1,npoints-1):
            tangents.append ( self.pointsTangentScaled( points[i-1], points[i+1], tightness) )
        tangents.append ( self.pointsTangentScaled( points[-2], points[-1], tightness) )

        h1 = lambda s: (2*(s**3))-(3*(s**2))+1
        h2 = lambda s: 3*(s**2)-2*(s**3)
        h3 = lambda s: (s**3)-(2*(s**2))+s
        h4 = lambda s: (s**3)-(s**2)

        for i in range(0,npoints-1):
            p0 = points[i]
            p1 = points[i+1]

            output.append(p0)

            # It would be better to divide each segment to steps according 
            # to tolerance but how to find maximum step size for tolerance?
            # It should be probably possible for with some math.
            #step = ???
            #dist = self.pointsDist(p0, p1)
            #if dist == 0 or dist < step:
                #continue
            #else:
                #t = float(step)/dist

            # for now we just make 50 points (more may become slow) and prune them using tolerance
            t = 1. / 50

            s = t

            tmpPoints = []
            output.append( tmpPoints )
            while s < 1:
                h1p1 = self.pointScalar( p0, h1(s) )
                h2p2 = self.pointScalar( p1, h2(s) )
                h3t1 = self.pointScalar( tangents[i], h3(s) )
                h4t2 = self.pointScalar( tangents[i+1], h4(s) ) 

                tmp1 = self.pointsAdd( h1p1, h2p2 )
                tmp2 = self.pointsAdd( h3t1, h4t2 )
                tmp = self.pointsAdd( tmp1, tmp2 )

                tmpPoints.append(tmp)

                s = s+t

        output.append(p1) # last point

        # now we have mix of points and point lists, we clean the lists
        # keeping the digitized points
        result = []
        for i in range(len(output)):
            p = output[i]
            if type(p) == list:
                pnts = [ output[i-1] ] + p + [ output[i+1] ]
                pnts = self.simplifyPoints ( pnts, tolerance )
                result.extend( pnts[1:-1] ) 
            else:
                result.append( p )

        return result

    def simplifyPoints( self, points, tolerance):
        geo = QgsGeometry.fromPolyline( points )
        geo = geo.simplify( tolerance );
        return geo.asPolyline()

    def pointScalar( self, p, k):
        return QgsPoint( p.x() * k, p.y() * k)

    def pointsAdd( self, p1, p2):
        return QgsPoint( p1.x() + p2.x(), p1.y() + p2.y() )

    def pointsTangentScaled(self, p1, p2, k ):
        x = p2.x()-p1.x()
        y = p2.y()-p1.y()
        return self.pointScalar( QgsPoint( x, y), k )

    def pointsDist(self, a, b):
        dx = a.x()-b.x()
        dy = a.y()-b.y()
        return math.sqrt( dx*dx + dy*dy )
