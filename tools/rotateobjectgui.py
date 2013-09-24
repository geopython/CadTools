# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_rotateobject import Ui_RotateObject
import os, sys

class RotateObjectGui(QDialog, Ui_RotateObject):

    okClicked = pyqtSignal(float)
    unsetTool = pyqtSignal()
  
    def __init__(self, parent, flags):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)
        
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.okButton.clicked.connect(self.accept)
        
        self.cancelButton = self.buttonBox.button(QDialogButtonBox.Cancel)
        self.cancelButton.clicked.connect(self.close)
        

    def initGui(self):
        self.rotationSpinBox.setMaximum(360)
        self.rotationSpinBox.setMinimum(-360)
        self.rotationSpinBox.setDecimals(10)
        pass

        
    def accept(self):
        self.okClicked.emit(self.rotationSpinBox.value())
        
    
    def close(self):
        self.unsetTool.emit()
