# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import math

from ui_showazimuth import Ui_ShowAzimuth

class ShowAzimuthGui(QDialog, QObject, Ui_ShowAzimuth):
    
    def __init__(self, parent, flags):
        QDialog.__init__(self, parent,  flags)
        self.setupUi(self)
    
    def initGui(self):
        pass
        
    def writeAzimuth(self,  az):
        try:
            az = float(az)
            self.lineGon.setText(str(200 * az / math.pi))
            self.lineDegrees.setText(str(180 * az / math.pi))            
            self.lineRadians.setText(str(az))            
        
        except (TypeError,  ValueError):
            self.lineGon.setText("Error.")
            self.lineDegrees.setText("Error.")            
            self.lineRadians.setText("Error.")
        
    @pyqtSignature("on_buttonClose_clicked()")    
    def on_buttonClose_clicked(self):
        self.emit(SIGNAL("unsetTool()"))         
        self.close()
        

