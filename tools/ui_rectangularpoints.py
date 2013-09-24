# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './tools/rectangularpoints.ui'
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

class Ui_RectangularPoints(object):
    def setupUi(self, RectangularPoints):
        RectangularPoints.setObjectName(_fromUtf8("RectangularPoints"))
        RectangularPoints.resize(388, 197)
        self.gridLayout_2 = QtGui.QGridLayout(RectangularPoints)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.chckBoxInvert = QtGui.QCheckBox(RectangularPoints)
        self.chckBoxInvert.setObjectName(_fromUtf8("chckBoxInvert"))
        self.horizontalLayout_4.addWidget(self.chckBoxInvert)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblA = QtGui.QLabel(RectangularPoints)
        self.lblA.setObjectName(_fromUtf8("lblA"))
        self.horizontalLayout.addWidget(self.lblA)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.sboxA = QtGui.QDoubleSpinBox(RectangularPoints)
        self.sboxA.setObjectName(_fromUtf8("sboxA"))
        self.horizontalLayout.addWidget(self.sboxA)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblO = QtGui.QLabel(RectangularPoints)
        self.lblO.setObjectName(_fromUtf8("lblO"))
        self.horizontalLayout_2.addWidget(self.lblO)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.sboxO = QtGui.QDoubleSpinBox(RectangularPoints)
        self.sboxO.setObjectName(_fromUtf8("sboxO"))
        self.horizontalLayout_2.addWidget(self.sboxO)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.btnAdd = QtGui.QPushButton(RectangularPoints)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout_3.addWidget(self.btnAdd)
        self.btnCancel = QtGui.QPushButton(RectangularPoints)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.horizontalLayout_3.addWidget(self.btnCancel)
        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(RectangularPoints)
        QtCore.QMetaObject.connectSlotsByName(RectangularPoints)

    def retranslateUi(self, RectangularPoints):
        RectangularPoints.setWindowTitle(_translate("RectangularPoints", "Rectangular Points", None))
        self.chckBoxInvert.setText(_translate("RectangularPoints", "Invert starting point", None))
        self.lblA.setText(_translate("RectangularPoints", "Abscissa (X):", None))
        self.lblO.setText(_translate("RectangularPoints", "Ordinate (Y):", None))
        self.btnAdd.setText(_translate("RectangularPoints", "Add", None))
        self.btnCancel.setText(_translate("RectangularPoints", "Cancel", None))

