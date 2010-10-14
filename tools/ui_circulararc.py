# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'circulararc.ui'
#
# Created: Thu Oct 14 22:00:49 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CircularArc(object):
    def setupUi(self, CircularArc):
        CircularArc.setObjectName("CircularArc")
        CircularArc.resize(288, 180)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CircularArc.sizePolicy().hasHeightForWidth())
        CircularArc.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(CircularArc)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(CircularArc)
        self.buttonBox.setEnabled(True)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(CircularArc)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioPitch = QtGui.QRadioButton(self.groupBox)
        self.radioPitch.setChecked(True)
        self.radioPitch.setObjectName("radioPitch")
        self.horizontalLayout.addWidget(self.radioPitch)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.spinBoxPitch = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBoxPitch.setEnabled(True)
        self.spinBoxPitch.setDecimals(1)
        self.spinBoxPitch.setMaximum(100.0)
        self.spinBoxPitch.setProperty("value", 2.0)
        self.spinBoxPitch.setObjectName("spinBoxPitch")
        self.horizontalLayout.addWidget(self.spinBoxPitch)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioAngle = QtGui.QRadioButton(self.groupBox)
        self.radioAngle.setObjectName("radioAngle")
        self.horizontalLayout_2.addWidget(self.radioAngle)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.spinBoxAngle = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBoxAngle.setDecimals(1)
        self.spinBoxAngle.setProperty("value", 1.0)
        self.spinBoxAngle.setObjectName("spinBoxAngle")
        self.horizontalLayout_2.addWidget(self.spinBoxAngle)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 3, 0, 1, 1)

        self.retranslateUi(CircularArc)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CircularArc.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CircularArc.accept)
        QtCore.QMetaObject.connectSlotsByName(CircularArc)

    def retranslateUi(self, CircularArc):
        CircularArc.setWindowTitle(QtGui.QApplication.translate("CircularArc", "Circular Arc", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("CircularArc", "Segmentation", None, QtGui.QApplication.UnicodeUTF8))
        self.radioPitch.setText(QtGui.QApplication.translate("CircularArc", "Pitch", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxPitch.setPrefix(QtGui.QApplication.translate("CircularArc", "Millimeter(s) ", None, QtGui.QApplication.UnicodeUTF8))
        self.radioAngle.setText(QtGui.QApplication.translate("CircularArc", "Angle", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxAngle.setPrefix(QtGui.QApplication.translate("CircularArc", "Degree(s) ", None, QtGui.QApplication.UnicodeUTF8))

