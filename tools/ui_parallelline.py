# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parallelline.ui'
#
# Created: Wed Oct 13 21:40:13 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ParallelLine(object):
    def setupUi(self, ParallelLine):
        ParallelLine.setObjectName("ParallelLine")
        ParallelLine.resize(382, 180)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ParallelLine.sizePolicy().hasHeightForWidth())
        ParallelLine.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(ParallelLine)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(ParallelLine)
        self.buttonBox.setEnabled(False)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(ParallelLine)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioFixed = QtGui.QRadioButton(self.groupBox)
        self.radioFixed.setChecked(True)
        self.radioFixed.setObjectName("radioFixed")
        self.horizontalLayout.addWidget(self.radioFixed)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.spinBoxDistance = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBoxDistance.setEnabled(True)
        self.spinBoxDistance.setDecimals(3)
        self.spinBoxDistance.setMaximum(99.99)
        self.spinBoxDistance.setObjectName("spinBoxDistance")
        self.horizontalLayout.addWidget(self.spinBoxDistance)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioVertex = QtGui.QRadioButton(self.groupBox)
        self.radioVertex.setObjectName("radioVertex")
        self.horizontalLayout_2.addWidget(self.radioVertex)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.btnSelectVertex = QtGui.QPushButton(self.groupBox)
        self.btnSelectVertex.setObjectName("btnSelectVertex")
        self.horizontalLayout_2.addWidget(self.btnSelectVertex)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 3, 0, 1, 1)

        self.retranslateUi(ParallelLine)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ParallelLine.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ParallelLine.accept)
        QtCore.QMetaObject.connectSlotsByName(ParallelLine)

    def retranslateUi(self, ParallelLine):
        ParallelLine.setWindowTitle(QtGui.QApplication.translate("ParallelLine", "Parallel Line", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("ParallelLine", "Parallel line", None, QtGui.QApplication.UnicodeUTF8))
        self.radioFixed.setText(QtGui.QApplication.translate("ParallelLine", "Fixed length", None, QtGui.QApplication.UnicodeUTF8))
        self.radioVertex.setText(QtGui.QApplication.translate("ParallelLine", "Snap to vertex", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectVertex.setText(QtGui.QApplication.translate("ParallelLine", "Select Vertex", None, QtGui.QApplication.UnicodeUTF8))

