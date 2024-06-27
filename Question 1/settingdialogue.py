# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings,parent,ti,col):
        self.parent = parent
        self.col = col
        Settings.setObjectName("Settings")
        Settings.resize(400, 100)
        self.gridLayoutWidget = QtWidgets.QWidget(parent=Settings)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")
        Settings.setLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=self.gridLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.mainLayout = QtWidgets.QFormLayout()
        self.mainLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.mainLayout.setObjectName("mainLayout")
        self.tIntervalLabel = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.tIntervalLabel.setObjectName("tIntervalLabel")
        self.mainLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.tIntervalLabel)
        self.graphColourLabel = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.graphColourLabel.setObjectName("graphColourLabel")
        self.mainLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.graphColourLabel)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.gridLayoutWidget)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox.setValue(ti)
        self.doubleSpinBox.setSingleStep(0.01)
        self.doubleSpinBox.valueChanged.connect(self.change)
        self.doubleSpinBox.setDecimals(2)
        self.doubleSpinBox.setRange(0.01,1.0)
        self.mainLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.doubleSpinBox)
        self.comboBox = QtWidgets.QComboBox(parent=self.gridLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(['Blue','Green','Red','Cyan','Purple','Yellow','Black','White'])
        self.comboBox.setCurrentIndex(col)
        self.comboBox.currentIndexChanged.connect(self.change)
        self.mainLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.comboBox)
        self.gridLayout.addLayout(self.mainLayout, 0, 0, 1, 1)

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept) # type: ignore
        self.buttonBox.rejected.connect(Settings.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.tIntervalLabel.setText(_translate("Settings", "Time step"))
        self.graphColourLabel.setText(_translate("Settings", "Graph colour"))
        self.comboBox.setCurrentIndex(self.col)


    def change(self):
        self.parent.newtint = self.doubleSpinBox.value()
        self.parent.newcol = self.comboBox.currentIndex()