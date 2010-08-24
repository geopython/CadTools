# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tools/arcintersection.ui'
#
# Created: Sun Jan 24 21:15:29 2010
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ArcIntersection(object):
    def setupUi(self, ArcIntersection):
        ArcIntersection.setObjectName("ArcIntersection")
        ArcIntersection.resize(391, 172)
        self.horizontalLayoutWidget = QtGui.QWidget(ArcIntersection)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 361, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblPnt1 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.lblPnt1.setObjectName("lblPnt1")
        self.horizontalLayout.addWidget(self.lblPnt1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.sboxPnt1 = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.sboxPnt1.setObjectName("sboxPnt1")
        self.horizontalLayout.addWidget(self.sboxPnt1)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(ArcIntersection)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 80, 361, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblPnt2 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.lblPnt2.setObjectName("lblPnt2")
        self.horizontalLayout_2.addWidget(self.lblPnt2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.sboxPnt2 = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget_2)
        self.sboxPnt2.setObjectName("sboxPnt2")
        self.horizontalLayout_2.addWidget(self.sboxPnt2)
        self.btnOK = QtGui.QPushButton(ArcIntersection)
        self.btnOK.setGeometry(QtCore.QRect(180, 130, 86, 30))
        self.btnOK.setObjectName("btnOK")
        self.btnCancel = QtGui.QPushButton(ArcIntersection)
        self.btnCancel.setGeometry(QtCore.QRect(280, 130, 86, 30))
        self.btnCancel.setObjectName("btnCancel")

        self.retranslateUi(ArcIntersection)
        QtCore.QMetaObject.connectSlotsByName(ArcIntersection)

    def retranslateUi(self, ArcIntersection):
        ArcIntersection.setWindowTitle(QtGui.QApplication.translate("ArcIntersection", "Arc Intersection", None, QtGui.QApplication.UnicodeUTF8))
        self.lblPnt1.setText(QtGui.QApplication.translate("ArcIntersection", "Distance to Point 1 (red): ", None, QtGui.QApplication.UnicodeUTF8))
        self.lblPnt2.setText(QtGui.QApplication.translate("ArcIntersection", "Distance to Point 2 (blue): ", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOK.setText(QtGui.QApplication.translate("ArcIntersection", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("ArcIntersection", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

