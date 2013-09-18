# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './tools/cadconsole.ui'
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

class Ui_CadConsole(object):
    def setupUi(self, CadConsole):
        CadConsole.setObjectName(_fromUtf8("CadConsole"))
        CadConsole.setWindowModality(QtCore.Qt.NonModal)
        CadConsole.setEnabled(True)
        CadConsole.resize(642, 126)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CadConsole.sizePolicy().hasHeightForWidth())
        CadConsole.setSizePolicy(sizePolicy)
        CadConsole.setMinimumSize(QtCore.QSize(101, 126))
        CadConsole.setMaximumSize(QtCore.QSize(524287, 524287))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.vboxlayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.textEdit = QtGui.QTextEdit(self.dockWidgetContents)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.vboxlayout.addWidget(self.textEdit)
        CadConsole.setWidget(self.dockWidgetContents)

        self.retranslateUi(CadConsole)
        QtCore.QMetaObject.connectSlotsByName(CadConsole)

    def retranslateUi(self, CadConsole):
        CadConsole.setWindowTitle(_translate("CadConsole", "CAD Console", None))

