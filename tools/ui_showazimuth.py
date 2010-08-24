# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'showazimuth.ui'
#
# Created: Fri Aug 13 18:00:03 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ShowAzimuth(object):
    def setupUi(self, ShowAzimuth):
        ShowAzimuth.setObjectName("ShowAzimuth")
        ShowAzimuth.resize(322, 223)
        self.gridLayout = QtGui.QGridLayout(ShowAzimuth)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtGui.QLabel(ShowAzimuth)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(ShowAzimuth)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lineGon = QtGui.QLineEdit(ShowAzimuth)
        self.lineGon.setEnabled(True)
        self.lineGon.setReadOnly(True)
        self.lineGon.setObjectName("lineGon")
        self.horizontalLayout.addWidget(self.lineGon)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(ShowAzimuth)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.lineDegrees = QtGui.QLineEdit(ShowAzimuth)
        self.lineDegrees.setReadOnly(True)
        self.lineDegrees.setObjectName("lineDegrees")
        self.horizontalLayout_2.addWidget(self.lineDegrees)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.buttonClose = QtGui.QPushButton(ShowAzimuth)
        self.buttonClose.setObjectName("buttonClose")
        self.horizontalLayout_3.addWidget(self.buttonClose)
        self.gridLayout.addLayout(self.horizontalLayout_3, 8, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtGui.QLabel(ShowAzimuth)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.lineRadians = QtGui.QLineEdit(ShowAzimuth)
        self.lineRadians.setObjectName("lineRadians")
        self.horizontalLayout_5.addWidget(self.lineRadians)
        self.gridLayout.addLayout(self.horizontalLayout_5, 6, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 1, 0, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 3, 0, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 5, 0, 1, 1)
        spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 7, 0, 1, 1)

        self.retranslateUi(ShowAzimuth)
        QtCore.QMetaObject.connectSlotsByName(ShowAzimuth)

    def retranslateUi(self, ShowAzimuth):
        ShowAzimuth.setWindowTitle(QtGui.QApplication.translate("ShowAzimuth", "Show Azimuth", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ShowAzimuth", "Azimuth from red to blue cross.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ShowAzimuth", "Azimuth [gon]: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ShowAzimuth", "Azimuth [degrees]: ", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonClose.setText(QtGui.QApplication.translate("ShowAzimuth", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ShowAzimuth", "Azimuth [radians]: ", None, QtGui.QApplication.UnicodeUTF8))

