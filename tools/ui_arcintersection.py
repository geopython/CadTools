# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './tools/arcintersection.ui'
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

class Ui_ArcIntersection(object):
    def setupUi(self, ArcIntersection):
        ArcIntersection.setObjectName(_fromUtf8("ArcIntersection"))
        ArcIntersection.resize(391, 172)
        self.horizontalLayoutWidget = QtGui.QWidget(ArcIntersection)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 361, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblPnt1 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.lblPnt1.setObjectName(_fromUtf8("lblPnt1"))
        self.horizontalLayout.addWidget(self.lblPnt1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.sboxPnt1 = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.sboxPnt1.setObjectName(_fromUtf8("sboxPnt1"))
        self.horizontalLayout.addWidget(self.sboxPnt1)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(ArcIntersection)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 80, 361, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblPnt2 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.lblPnt2.setObjectName(_fromUtf8("lblPnt2"))
        self.horizontalLayout_2.addWidget(self.lblPnt2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.sboxPnt2 = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget_2)
        self.sboxPnt2.setObjectName(_fromUtf8("sboxPnt2"))
        self.horizontalLayout_2.addWidget(self.sboxPnt2)
        self.btnOK = QtGui.QPushButton(ArcIntersection)
        self.btnOK.setGeometry(QtCore.QRect(180, 130, 86, 30))
        self.btnOK.setObjectName(_fromUtf8("btnOK"))
        self.btnCancel = QtGui.QPushButton(ArcIntersection)
        self.btnCancel.setGeometry(QtCore.QRect(280, 130, 86, 30))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))

        self.retranslateUi(ArcIntersection)
        QtCore.QMetaObject.connectSlotsByName(ArcIntersection)

    def retranslateUi(self, ArcIntersection):
        ArcIntersection.setWindowTitle(_translate("ArcIntersection", "Arc Intersection", None))
        self.lblPnt1.setText(_translate("ArcIntersection", "Distance to Point 1 (red): ", None))
        self.lblPnt2.setText(_translate("ArcIntersection", "Distance to Point 2 (blue): ", None))
        self.btnOK.setText(_translate("ArcIntersection", "OK", None))
        self.btnCancel.setText(_translate("ArcIntersection", "Cancel", None))

