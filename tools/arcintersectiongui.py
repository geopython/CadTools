# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from ui_arcintersection import Ui_ArcIntersection

class ArcIntersectionGui(QDialog, QObject, Ui_ArcIntersection):
    MSG_BOX_TITLE = "Arc Intersection"
    
    def __init__(self, parent,  fl):
        QDialog.__init__(self, parent,  fl)
        self.setupUi(self)
    
    def initGui(self):
        self.sboxPnt1.setMaximum(10000000)
        self.sboxPnt1.setDecimals(4)
        
        self.sboxPnt2.setMaximum(10000000)
        self.sboxPnt2.setDecimals(4)        
        
    @pyqtSignature("on_btnOK_clicked()")    
    def on_btnOK_clicked(self):
        self.emit(SIGNAL("distancesFromPoints(double, double)"),  self.sboxPnt1.value(),  self.sboxPnt2.value())        
        self.close()
        
    @pyqtSignature("on_btnCancel_clicked()")    
    def on_btnCancel_clicked(self): 
        self.emit(SIGNAL("closeArcIntersectionGui()"))  
        self.emit(SIGNAL("unsetTool()")) 
        self.close()
