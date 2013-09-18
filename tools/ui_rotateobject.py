# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './tools/rotateobject.ui'
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

class Ui_RotateObject(object):
    def setupUi(self, RotateObject):
        RotateObject.setObjectName(_fromUtf8("RotateObject"))
        RotateObject.resize(252, 82)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RotateObject.sizePolicy().hasHeightForWidth())
        RotateObject.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(RotateObject)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(RotateObject)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.rotationSpinBox = QtGui.QDoubleSpinBox(RotateObject)
        self.rotationSpinBox.setObjectName(_fromUtf8("rotationSpinBox"))
        self.horizontalLayout_2.addWidget(self.rotationSpinBox)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RotateObject)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(RotateObject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RotateObject.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RotateObject.accept)
        QtCore.QMetaObject.connectSlotsByName(RotateObject)

    def retranslateUi(self, RotateObject):
        RotateObject.setWindowTitle(_translate("RotateObject", "Rotate Feature", None))
        self.label.setText(_translate("RotateObject", "Rotation angle [deg]: ", None))

