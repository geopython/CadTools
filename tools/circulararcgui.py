# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_circulararc import Ui_CircularArc
import os, sys

class CircularArcGui(QDialog, Ui_CircularArc):

    def __init__(self, parent, flags):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.method = "fixed"

        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)

        self.cancelButton = self.buttonBox.button(QDialogButtonBox.Cancel)
        self.connect(self.cancelButton, SIGNAL("clicked()"), self.close)        


    def initGui(self):
        self.spinBoxPitch.setMinimum(0.1)
        self.spinBoxPitch.setMaximum(1000)
        self.spinBoxPitch.setDecimals(1)
        
        self.spinBoxAngle.setMinimum(1)
        self.spinBoxAngle.setMaximum(90)
        self.spinBoxAngle.setDecimals(1)        

        self.radioPitch.setChecked(True)
        self.radioAngle.setChecked(False)
        
        self.spinBoxPitch.setEnabled(True)              
        self.spinBoxAngle.setEnabled(False)  

        self.buttonBox.setEnabled(True)
        
        self.method = "pitch"


    @pyqtSignature("on_radioPitch_clicked()")    
    def on_radioPitch_clicked(self):     
        self.method = "pitch"
        self.spinBoxAngle.setEnabled(False)
        self.spinBoxPitch.setEnabled(True)


    @pyqtSignature("on_radioAngle_clicked()")    
    def on_radioAngle_clicked(self):      
        self.method = "angle"
        self.spinBoxAngle.setEnabled(True)
        self.spinBoxPitch.setEnabled(False)


#    @pyqtSignature("on_btnSelectVertex_clicked()") 
#    def on_btnSelectVertex_clicked(self):
#        self.method = "vertex"
#        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)   
#        self.emit( SIGNAL("btnSelectVertex_clicked()") )
#
#
    def accept(self):
        if self.method == "pitch":
            segValue = self.spinBoxPitch.value()
        elif self.method == "angle":
            segValue = self.spinBoxAngle.value()
        else:
            segValue = 1
            self.emit(SIGNAL("unsetTool()")) 
        self.emit( SIGNAL("okClicked(QString, double)"),  self.method,  segValue)
        pass


    def close(self):
        self.emit(SIGNAL("unsetTool()")) 
        pass
