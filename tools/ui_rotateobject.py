# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rotateobject.ui'
#
# Created: Sat Aug 14 16:08:54 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RotateObject(object):
    def setupUi(self, RotateObject):
        RotateObject.setObjectName("RotateObject")
        RotateObject.resize(252, 82)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RotateObject.sizePolicy().hasHeightForWidth())
        RotateObject.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(RotateObject)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(RotateObject)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.rotationSpinBox = QtGui.QDoubleSpinBox(RotateObject)
        self.rotationSpinBox.setObjectName("rotationSpinBox")
        self.horizontalLayout_2.addWidget(self.rotationSpinBox)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RotateObject)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(RotateObject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), RotateObject.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), RotateObject.accept)
        QtCore.QMetaObject.connectSlotsByName(RotateObject)

    def retranslateUi(self, RotateObject):
        RotateObject.setWindowTitle(QtGui.QApplication.translate("RotateObject", "Rotate Feature", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RotateObject", "Rotation angle [deg]: ", None, QtGui.QApplication.UnicodeUTF8))

