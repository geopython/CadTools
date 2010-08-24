# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_rotateobject import Ui_RotateObject
import os, sys

class RotateObjectGui(QDialog, Ui_RotateObject):
  
    def __init__(self, parent, flags):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)
        
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)
        
        self.cancelButton = self.buttonBox.button(QDialogButtonBox.Cancel)
        self.connect(self.cancelButton, SIGNAL("clicked()"), self.close)        
        

    def initGui(self):
        self.rotationSpinBox.setMaximum(360)
        self.rotationSpinBox.setMinimum(-360)
        self.rotationSpinBox.setDecimals(10)
        pass

        
    def accept(self):
        self.emit( SIGNAL("okClicked(double)"),  self.rotationSpinBox.value())
        
    
    def close(self):
        self.emit(SIGNAL("unsetTool()")) 
