# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './cadtoolsabout.ui'
#
# Created: Wed Sep 18 17:02:25 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CadToolsAbout(object):
    def setupUi(self, CadToolsAbout):
        CadToolsAbout.setObjectName(_fromUtf8("CadToolsAbout"))
        CadToolsAbout.resize(285, 335)
        self.gridlayout = QtGui.QGridLayout(CadToolsAbout)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.txtAbout = QtGui.QTextEdit(CadToolsAbout)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.txtAbout.setPalette(palette)
        self.txtAbout.setAutoFillBackground(True)
        self.txtAbout.setFrameShape(QtGui.QFrame.NoFrame)
        self.txtAbout.setFrameShadow(QtGui.QFrame.Plain)
        self.txtAbout.setReadOnly(True)
        self.txtAbout.setObjectName(_fromUtf8("txtAbout"))
        self.gridlayout.addWidget(self.txtAbout, 2, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 1, 1, 1)
        self.btnHelp = QtGui.QPushButton(CadToolsAbout)
        self.btnHelp.setObjectName(_fromUtf8("btnHelp"))
        self.gridlayout.addWidget(self.btnHelp, 4, 0, 1, 1)
        self.btnClose = QtGui.QPushButton(CadToolsAbout)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridlayout.addWidget(self.btnClose, 4, 2, 1, 1)
        self.btnWeb = QtGui.QPushButton(CadToolsAbout)
        self.btnWeb.setObjectName(_fromUtf8("btnWeb"))
        self.gridlayout.addWidget(self.btnWeb, 4, 1, 1, 1)
        self.lblVersion = QtGui.QLabel(CadToolsAbout)
        self.lblVersion.setObjectName(_fromUtf8("lblVersion"))
        self.gridlayout.addWidget(self.lblVersion, 1, 0, 1, 2)
        self.lblTitle = QtGui.QLabel(CadToolsAbout)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lblTitle.setFont(font)
        self.lblTitle.setTextFormat(QtCore.Qt.RichText)
        self.lblTitle.setObjectName(_fromUtf8("lblTitle"))
        self.gridlayout.addWidget(self.lblTitle, 0, 0, 1, 2)

        self.retranslateUi(CadToolsAbout)
        QtCore.QObject.connect(self.btnClose, QtCore.SIGNAL(_fromUtf8("clicked()")), CadToolsAbout.reject)
        QtCore.QMetaObject.connectSlotsByName(CadToolsAbout)

    def retranslateUi(self, CadToolsAbout):
        CadToolsAbout.setWindowTitle(_translate("CadToolsAbout", "CadTools About", None))
        self.txtAbout.setHtml(_translate("CadToolsAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:9pt;\"></p></body></html>", None))
        self.btnHelp.setText(_translate("CadToolsAbout", "Help", None))
        self.btnClose.setText(_translate("CadToolsAbout", "Close", None))
        self.btnWeb.setText(_translate("CadToolsAbout", "Web", None))
        self.lblVersion.setText(_translate("CadToolsAbout", "Version x.x-xxxxxx", None))
        self.lblTitle.setText(_translate("CadToolsAbout", "CadTools", None))

