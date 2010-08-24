# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from vertexfindertool import VertexFinderTool
from ui_orthogonaltraverse import Ui_OrthogonalTraverse

class OrthogonalTraverseGui(QDialog, QObject, Ui_OrthogonalTraverse):
    MSG_BOX_TITLE = "Orthogonal Traverse"
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
    
    def initGui(self, p1, p2):
        self.validator = QDoubleValidator(self.lineEditStartX)
        self.validator.setRange(-999999999.999, 999999999.999, 4)
        self.lineEditStartX.setValidator(self.validator)        
        self.lineEditStartY.setValidator(self.validator)  
        self.lineEditEndX.setValidator(self.validator)  
        self.lineEditEndY.setValidator(self.validator)  
        
        # good:
        #traverseStr = "-6.20 +2.81 -5.03 -10.64"
        traverseStr = "10.64 5.03 2.81 -6.2"
        # evil:
        #traverseStr = "-6.21 +2.82 -5.04 -10.65"        
        #self.lineEditTraverse.setText(str(traverseStr))
        
        #agag = validator.validate('1234.3', 3)
        #QMessageBox.information(None,  "Cancel", str(agag))
        
        # traverse already adjusted?
        self.adjusted = False
        
        if p1 <> None:
            self.lineEditStartX.setText(str(p1.x()))
            self.lineEditStartY.setText(str(p1.y()))
        
        if p2 <> None:
            self.lineEditEndX.setText(str(p2.x()))
            self.lineEditEndY.setText(str(p2.y()))
            
        # Connect to signal to remember user that some data has changed
        self.connect(self.lineEditTraverse, SIGNAL("textChanged(const QString &)"), self.textHasChanged) 
        self.connect(self.lineEditStartX, SIGNAL("textChanged(const QString &)"), self.textHasChanged) 
        self.connect(self.lineEditStartY, SIGNAL("textChanged(const QString &)"), self.textHasChanged) 
        self.connect(self.lineEditEndX, SIGNAL("textChanged(const QString &)"), self.textHasChanged) 
        self.connect(self.lineEditEndY, SIGNAL("textChanged(const QString &)"), self.textHasChanged) 
            
        pass
        
    def textHasChanged(self):
        self.adjusted = False
        
    def checkInputData(self):
        # first we need to check if the start- and endpoint are different
        # and if we have valid float values
        errFloat = 0
        try:
            x1 = float(self.lineEditStartX.text())
            y1 = float(self.lineEditStartY.text())
        
            x2 = float(self.lineEditEndX.text())
            y2 = float(self.lineEditEndY.text())           
            
            if x1 == x2 and y1 == y2:
                QMessageBox.information(None,  "Warning", "Starting- and Endpoint are equal. This is not yet supported.")
                return 0
            
        except ValueError:
            errFloat = 1
            
        if errFloat == 1:
            QMessageBox.information(None,  "Warning", "No valid coordinates found.")
            return 0
            
        # Then we need to check if the traverse string is valid.
        
        if len(self.lineEditTraverse.text()) == 0:
            QMessageBox.information(None,  "Warning", "No valid traverse found.")
            return 0
        
        trv = str(self.lineEditTraverse.text()).strip()
        measurementsStrList = trv.split()

        # Less than 2 measurements do not work
        if len(measurementsStrList) < 2:
            QMessageBox.information(None,  "Warning", "Less than 2 measurements are not allowed.")
            return 0
        
        # Strings?
        errFloat = 0
        for i in measurementsStrList:
            try:
                f = float(i)
                if f == 0:
                    errFloat = 1
            except ValueError:
                errFloat = 1
                            
        if errFloat == 1:
            QMessageBox.information(None,  "Warning", "No valid traverse found.")
            return 0
        
        if float(measurementsStrList[0]) == 0:
            QMessageBox.information(None,  "Warning", "First measurement is zero")
            return 0
        
        # Everything is ok
        return 1

    @pyqtSignature("on_btnEql_clicked()")    
    def on_btnEql_clicked(self):
        isValid = self.checkInputData()
        if isValid == 1:
            self.emit(SIGNAL("sendTraverse(QString, double, double, double, double, bool, bool)"), str(self.lineEditTraverse.text()),  float(self.lineEditStartX.text()),  float(self.lineEditStartY.text()),  float(self.lineEditEndX.text()),  float(self.lineEditEndY.text()), True, False) 
            self.adjusted = True
            print "emitiert...EqlBtn"
        else:
            return

    @pyqtSignature("on_btnOK_clicked()")    
    def on_btnOK_clicked(self):
        
        isValid = self.checkInputData()
        if isValid == 1:
            if self.adjusted == True:
                self.emit(SIGNAL("sendTraverse(QString, double, double, double, double, bool, bool)"), str(self.lineEditTraverse.text()),  float(self.lineEditStartX.text()),  float(self.lineEditStartY.text()),  float(self.lineEditEndX.text()),  float(self.lineEditEndY.text()), True, True) 
            else:
                reply = QMessageBox.question(self, 'Message',  "Traverse is not adjusted. Do you want to adjust it first?", QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.emit(SIGNAL("sendTraverse(QString, double, double, double, double, bool, bool)"), str(self.lineEditTraverse.text()),  float(self.lineEditStartX.text()),  float(self.lineEditStartY.text()),  float(self.lineEditEndX.text()),  float(self.lineEditEndY.text()), True, True) 
                else:
                    self.emit(SIGNAL("sendTraverse(QString, double, double, double, double, bool, bool)"), str(self.lineEditTraverse.text()),  float(self.lineEditStartX.text()),  float(self.lineEditStartY.text()),  float(self.lineEditEndX.text()),  float(self.lineEditEndY.text()), False, True) 
            print "emitiert...OkBtn"
        else:
            return
        
        #self.close()
        
    @pyqtSignature("on_btnCancel_clicked()")    
    def on_btnCancel_clicked(self): 
        self.emit(SIGNAL("closeOrthogonalTraverseGui()"))  
        self.emit(SIGNAL("unsetTool()")) 
        self.close()
