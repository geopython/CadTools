# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cadconsole.ui'
#
# Created: Sun Mar 21 17:31:50 2010
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CadConsole(object):
    def setupUi(self, CadConsole):
        CadConsole.setObjectName("CadConsole")
        CadConsole.setWindowModality(QtCore.Qt.NonModal)
        CadConsole.setEnabled(True)
        CadConsole.resize(642, 193)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CadConsole.sizePolicy().hasHeightForWidth())
        CadConsole.setSizePolicy(sizePolicy)
        CadConsole.setMinimumSize(QtCore.QSize(101, 126))
        CadConsole.setMaximumSize(QtCore.QSize(524287, 524287))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.vboxlayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.vboxlayout.setObjectName("vboxlayout")
##        self.textEdit = QtGui.QTextEdit(self.dockWidgetContents)
##        self.textEdit.setObjectName("textEdit")
##        self.vboxlayout.addWidget(self.textEdit)
        CadConsole.setWidget(self.dockWidgetContents)

        self.retranslateUi(CadConsole)
        QtCore.QMetaObject.connectSlotsByName(CadConsole)

    def retranslateUi(self, CadConsole):
        CadConsole.setWindowTitle(QtGui.QApplication.translate("CadConsole", "CAD Console", None, QtGui.QApplication.UnicodeUTF8))

