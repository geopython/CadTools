# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rectangularpoints.ui'
#
# Created: Sat Jun  5 20:16:12 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RectangularPoints(object):
    def setupUi(self, RectangularPoints):
        RectangularPoints.setObjectName("RectangularPoints")
        RectangularPoints.resize(388, 197)
        self.gridLayout_2 = QtGui.QGridLayout(RectangularPoints)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.chckBoxInvert = QtGui.QCheckBox(RectangularPoints)
        self.chckBoxInvert.setObjectName("chckBoxInvert")
        self.horizontalLayout_4.addWidget(self.chckBoxInvert)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblA = QtGui.QLabel(RectangularPoints)
        self.lblA.setObjectName("lblA")
        self.horizontalLayout.addWidget(self.lblA)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.sboxA = QtGui.QDoubleSpinBox(RectangularPoints)
        self.sboxA.setObjectName("sboxA")
        self.horizontalLayout.addWidget(self.sboxA)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblO = QtGui.QLabel(RectangularPoints)
        self.lblO.setObjectName("lblO")
        self.horizontalLayout_2.addWidget(self.lblO)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.sboxO = QtGui.QDoubleSpinBox(RectangularPoints)
        self.sboxO.setObjectName("sboxO")
        self.horizontalLayout_2.addWidget(self.sboxO)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.btnAdd = QtGui.QPushButton(RectangularPoints)
        self.btnAdd.setObjectName("btnAdd")
        self.horizontalLayout_3.addWidget(self.btnAdd)
        self.btnCancel = QtGui.QPushButton(RectangularPoints)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_3.addWidget(self.btnCancel)
        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(RectangularPoints)
        QtCore.QMetaObject.connectSlotsByName(RectangularPoints)

    def retranslateUi(self, RectangularPoints):
        RectangularPoints.setWindowTitle(QtGui.QApplication.translate("RectangularPoints", "Rectangular Points", None, QtGui.QApplication.UnicodeUTF8))
        self.chckBoxInvert.setText(QtGui.QApplication.translate("RectangularPoints", "Invert starting point", None, QtGui.QApplication.UnicodeUTF8))
        self.lblA.setText(QtGui.QApplication.translate("RectangularPoints", "Abscissa (X):", None, QtGui.QApplication.UnicodeUTF8))
        self.lblO.setText(QtGui.QApplication.translate("RectangularPoints", "Ordinate (Y):", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd.setText(QtGui.QApplication.translate("RectangularPoints", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("RectangularPoints", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

