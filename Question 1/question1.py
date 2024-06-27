from PyQt6 import QtCore, QtGui, QtWidgets

import json
import math
import sys
import os
import xlsxwriter

import numpy as np

import matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

from matplotlib.figure import Figure

matplotlib.use('QtAgg')


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Ui_Table(object):
    def setupUi(self, Table, t, ux, uy, x, y, g):
        Table.setObjectName("Table")
        Table.resize(950, 450)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        Table.setLayout(self.verticalLayout)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.DataTable = QtWidgets.QTableWidget()
        self.DataTable.setObjectName("DataTable")
        self.DataTable.setColumnCount(6)
        self.DataTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.DataTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.DataTable.setHorizontalHeaderItem(5, item)
        colwidth = [80, 160, 160, 160, 160, 160]
        for i in range(6):
            self.DataTable.setColumnWidth(i, colwidth[i])
        self.verticalLayout.addWidget(self.DataTable)
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setEnabled(True)
        self.buttonBox.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedKingdom))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.clicked.connect(Table.reject)

        self.retranslateUi(Table)
        QtCore.QMetaObject.connectSlotsByName(Table)
        self.table(t, ux, uy, x, y, g)

    def retranslateUi(self, Table):
        _translate = QtCore.QCoreApplication.translate
        Table.setWindowTitle(_translate("Table", "Data"))
        Table.setWindowIcon(QtGui.QIcon(resource_path("Mainicon.png")))
        item = self.DataTable.horizontalHeaderItem(0)
        item.setText(_translate("Table", "t"))
        item = self.DataTable.horizontalHeaderItem(1)
        item.setText(_translate("Table", "vx"))
        item = self.DataTable.horizontalHeaderItem(2)
        item.setText(_translate("Table", "vy"))
        item = self.DataTable.horizontalHeaderItem(3)
        item.setText(_translate("Table", "v"))
        item = self.DataTable.horizontalHeaderItem(4)
        item.setText(_translate("Table", "x"))
        item = self.DataTable.horizontalHeaderItem(5)
        item.setText(_translate("Table", "y"))

    def table(self, t, ux, uy, x, y, g):

        self.DataTable.setRowCount(len(t))
        for row in range(len(t)):
            time = t[row]
            self.DataTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(round(time, 2))))
            self.DataTable.setItem(row, 1, QtWidgets.QTableWidgetItem(str(ux)))
            self.DataTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(uy - g * time)))
            self.DataTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(math.sqrt(ux ** 2 + (uy - g * time) ** 2))))
            self.DataTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(x[row])))
            self.DataTable.setItem(row, 5, QtWidgets.QTableWidgetItem(str(y[row])))
        self.delegate = ReadOnlyDelegate()
        self.DataTable.setItemDelegate(self.delegate)


class Ui_Equation(object):
    def setupUi(self, Equation):
        Equation.setObjectName("Equation")
        Equation.resize(339, 377)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Equation.sizePolicy().hasHeightForWidth())
        Equation.setSizePolicy(sizePolicy)
        Equation.setMinimumSize(QtCore.QSize(339, 377))
        Equation.setMaximumSize(QtCore.QSize(339, 16777215))
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=Equation)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 341, 381))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label.setAutoFillBackground(True)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(resource_path("Equations.png")))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(Equation)
        QtCore.QMetaObject.connectSlotsByName(Equation)

    def retranslateUi(self, Equation):
        _translate = QtCore.QCoreApplication.translate
        Equation.setWindowTitle(_translate("Equation", "Equations"))
        Equation.setWindowIcon(QtGui.QIcon(resource_path("Mainicon.png")))


class Ui_Settings(object):
    def setupUi(self, Settings, parent, ti, col):
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
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)
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
        self.doubleSpinBox.setRange(0.01, 1.0)
        self.mainLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.doubleSpinBox)
        self.comboBox = QtWidgets.QComboBox(parent=self.gridLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(['Blue', 'Green', 'Red', 'Cyan', 'Purple', 'Yellow', 'Black', 'White'])
        self.comboBox.setCurrentIndex(col)
        self.comboBox.currentIndexChanged.connect(self.change)
        self.mainLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.comboBox)
        self.gridLayout.addLayout(self.mainLayout, 0, 0, 1, 1)

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)  # type: ignore
        self.buttonBox.rejected.connect(Settings.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        Settings.setWindowIcon(QtGui.QIcon(resource_path("Mainicon.png")))
        self.tIntervalLabel.setText(_translate("Settings", "Time step"))
        self.graphColourLabel.setText(_translate("Settings", "Graph colour"))
        self.comboBox.setCurrentIndex(self.col)

    def change(self):
        self.parent.newtint = self.doubleSpinBox.value()
        self.parent.newcol = self.comboBox.currentIndex()


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        super(MplCanvas, self).__init__(self.fig)

    def tight(self, p, wp, hp):
        self.fig.tight_layout(pad = p, w_pad = wp, h_pad=hp)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.changed = False
        self.readjson()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(14)
        MainWindow.setFont(font)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedKingdom))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonFollowStyle)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.mainLayoutWidget.setObjectName("mainLayoutWidget")
        self.mainLayout = QtWidgets.QGridLayout(self.mainLayoutWidget)
        self.mainLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setObjectName("mainLayout")
        self.inputLayout = QtWidgets.QFormLayout()
        self.inputLayout.setObjectName("inputLayout")
        self.launchAngleDegreeLabel = QtWidgets.QLabel(parent=self.mainLayoutWidget)
        self.launchAngleDegreeLabel.setObjectName("launchAngleDegreeLabel")
        self.inputLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.launchAngleDegreeLabel)
        self.launchAngelRadianLabel = QtWidgets.QLabel(parent=self.mainLayoutWidget)
        self.launchAngelRadianLabel.setObjectName("launchAngelRadianLabel")
        self.inputLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.launchAngelRadianLabel)
        self.RadSpinbox = QtWidgets.QDoubleSpinBox(parent=self.mainLayoutWidget)
        self.RadSpinbox.setDecimals(12)
        self.RadSpinbox.setRange(0, math.pi / 2)
        self.RadSpinbox.setValue(math.pi / 4)
        self.RadSpinbox.setSingleStep(math.pi / 180)
        self.RadSpinbox.valueChanged.connect(self.radtodeg)
        self.inputLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.RadSpinbox)
        self.launchSpeedMs1Label = QtWidgets.QLabel(parent=self.mainLayoutWidget)
        self.launchSpeedMs1Label.setObjectName("launchSpeedMs1Label")
        self.inputLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.launchSpeedMs1Label)
        self.launchHeightMLabel = QtWidgets.QLabel(parent=self.mainLayoutWidget)
        self.launchHeightMLabel.setObjectName("launchHeightMLabel")
        self.inputLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.launchHeightMLabel)
        self.gMs2Label = QtWidgets.QLabel(parent=self.mainLayoutWidget)
        self.gMs2Label.setObjectName("gMs2Label")
        self.inputLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.gMs2Label)
        self.GSpinBox = QtWidgets.QDoubleSpinBox(parent=self.mainLayoutWidget)
        self.GSpinBox.setMaximum(9999999999.0)
        self.GSpinBox.setSingleStep(0.1)
        self.GSpinBox.setProperty("value", 9.81)
        self.GSpinBox.setObjectName("GSpinBox")
        self.GSpinBox.valueChanged.connect(self.updategraph)
        self.GSpinBox.setRange(0, 99999999)
        self.inputLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.GSpinBox)
        self.DegSpinbox = QtWidgets.QDoubleSpinBox(parent=self.mainLayoutWidget)
        self.DegSpinbox.setDecimals(2)
        self.DegSpinbox.setValue(45)
        self.DegSpinbox.setRange(0, 90)
        self.DegSpinbox.setSingleStep(1.0)
        self.DegSpinbox.valueChanged.connect(self.degtorad)
        self.inputLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.DegSpinbox)
        self.SpeedSpinBox = QtWidgets.QDoubleSpinBox(parent=self.mainLayoutWidget)
        self.SpeedSpinBox.setSingleStep(1)
        self.SpeedSpinBox.setProperty("value", 10.0)
        self.SpeedSpinBox.setObjectName("SpeedSpinBox")
        self.SpeedSpinBox.valueChanged.connect(self.updategraph)
        self.SpeedSpinBox.setRange(0, 99999999)
        self.inputLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.SpeedSpinBox)
        self.HeightSpinBox = QtWidgets.QDoubleSpinBox(parent=self.mainLayoutWidget)
        self.HeightSpinBox.setProperty("value", 10.0)
        self.HeightSpinBox.setObjectName("HeightSpinBox")
        self.HeightSpinBox.valueChanged.connect(self.updategraph)
        self.HeightSpinBox.setRange(0, 99999999)
        self.inputLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.HeightSpinBox)
        self.mainLayout.addLayout(self.inputLayout, 0, 0, 1, 1)

        self.Graph = MplCanvas(self, width=7, height=5, dpi=100)
        self.Graph.setObjectName("Graph")
        self.Graph.tight(1.5, 0, 0)
        self.mainLayout.addWidget(self.Graph, 0, 1, 2, 1)
        toolbar = NavigationToolbar2QT(self.Graph, MainWindow)
        self.mainLayout.addWidget(toolbar, 2, 1, 3, 1)
        self.mainLayout.setColumnMinimumWidth(0, 320)
        self.mainLayout.setRowStretch(1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menuGuide = QtWidgets.QMenu(parent=self.menubar)
        self.menuGuide.setObjectName('menuGuide')
        self.menuData = QtWidgets.QMenu(parent=self.menubar)
        self.menuData.setObjectName("menuData")
        self.menuOptions = QtWidgets.QMenu(parent=self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionEquation = QtGui.QAction(parent=MainWindow)
        self.actionEquation.setObjectName("actionEquation")
        self.actionShow_data = QtGui.QAction("Show data")
        self.actionShow_data.setObjectName("actionShow_data")
        self.actionExport_data = QtGui.QAction(parent=MainWindow)
        self.actionExport_data.setObjectName("actionExport_data")
        self.actionSettings = QtGui.QAction(parent=MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.menuGuide.addAction(self.actionEquation)
        self.menuData.addAction(self.actionShow_data)
        self.menuData.addAction(self.actionExport_data)
        self.menuOptions.addAction(self.actionSettings)
        self.menubar.addAction(self.menuGuide.menuAction())
        self.menubar.addAction(self.menuData.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.centralwidget.setLayout(self.mainLayout)

        self.updategraph()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Challenge #1"))
        MainWindow.setWindowIcon(QtGui.QIcon(resource_path("Mainicon.png")))
        self.launchAngleDegreeLabel.setText(_translate("MainWindow", "Launch angle (degree)"))
        self.launchAngelRadianLabel.setText(_translate("MainWindow", "Launch angle (radian)"))
        self.launchSpeedMs1Label.setText(_translate("MainWindow", "Launch speed (ms-1)"))
        self.launchHeightMLabel.setText(_translate("MainWindow", "Launch height (m)"))
        self.gMs2Label.setText(_translate("MainWindow", "g (ms-2)"))
        self.menuGuide.setTitle("About")
        self.menuData.setTitle(_translate("MainWindow", "Data"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.actionEquation.setText("Show Equations")
        self.actionEquation.setIcon(QtGui.QIcon(resource_path("Eq.png")))
        self.actionEquation.triggered.connect(self.showeq)
        self.actionShow_data.setText(_translate("MainWindow", "Show data table"))
        self.actionShow_data.setShortcut("Ctrl+T")
        self.actionShow_data.setIcon(QtGui.QIcon(resource_path("Table.png")))
        self.actionShow_data.triggered.connect(self.showtable)
        self.actionExport_data.setText(_translate("MainWindow", "Export data"))
        self.actionExport_data.setShortcut("Ctrl+E")
        self.actionExport_data.setIcon(QtGui.QIcon(resource_path("Export.png")))
        self.actionExport_data.triggered.connect(self.exporttable)
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionSettings.triggered.connect(self.asksettings)
        self.actionSettings.setIcon(QtGui.QIcon(resource_path("Settings.png")))
        self.actionSettings.setShortcut("Ctrl+Shift+S")

    def asksettings(self):  # startup another dialog
        self.newtint = 0.01
        self.newcol = 0
        Dialog = QtWidgets.QDialog()
        ui = Ui_Settings()
        ui.setupUi(Dialog, self, self.tint, self.col)
        if Dialog.exec():  # check if OK is pressed
            self.tint = self.newtint
            self.col = self.newcol
            f = open("settings.json", 'w')
            json.dump({'tInterval': self.tint, 'GraphColour': self.col}, f)
            f.close()
            self.updategraph()

    def readjson(self):  # read from settings.json for self.tint and self.col
        try:
            f = open("settings.json", 'r')
            data = json.load(f)
            f.close()
            self.tint = data['tInterval']
            self.col = data['GraphColour']
        except FileNotFoundError:
            data = {'tInterval': 0.01, 'GraphColour': 0}
            f = open("settings.json", 'w')
            json.dump(data, f)
            f.close()
            self.tint = 0.01
            self.col = 0

    def degtorad(self):
        if not self.changed:  # only do once
            self.changed = True
            self.RadSpinbox.setValue(self.DegSpinbox.value() / 180 * math.pi)
            self.updategraph()
        else:
            self.changed = False

    def radtodeg(self):
        if not self.changed:  # only do once
            self.changed = True
            self.DegSpinbox.setValue(self.RadSpinbox.value() / math.pi * 180)
            self.updategraph()
        else:
            self.changed = False

    def updategraph(self):
        self.Graph.axes.cla()
        self.ux = self.SpeedSpinBox.value() * math.cos(self.RadSpinbox.value())
        self.uy = self.SpeedSpinBox.value() * math.sin(self.RadSpinbox.value())
        self.h = self.HeightSpinBox.value()
        self.g = self.GSpinBox.value()
        tmax = (self.uy + math.sqrt(self.uy * self.uy + 2 * self.g * self.h)) / self.g
        self.t = np.arange(0, tmax+1, self.tint)
        self.x = self.ux * self.t
        self.y = self.h + self.uy * self.t - 0.5 * self.g * self.t * self.t
        ymax = self.uy * self.uy / 2 / self.g + self.h
        self.Graph.axes.plot(self.x, self.y, 'bgrcmykw'[self.col])
        self.Graph.axes.set_xlim(0, math.ceil(self.ux * tmax * 1.1))
        self.Graph.axes.set_ylim(0, math.ceil(ymax * 1.1))
        self.Graph.axes.set_title("Projectile motion model - no air resistance")
        self.Graph.axes.set_xlabel("x / m")
        self.Graph.axes.set_ylabel("y / m")
        self.Graph.draw()

    def showeq(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Equation()
        ui.setupUi(Dialog)
        Dialog.exec()

    def showtable(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Table()
        ui.setupUi(Dialog, self.t, self.ux, self.uy, self.x, self.y, self.g)
        Dialog.exec()

    def exporttable(self):
        tablefilter = "Excel file (*.xlsx)"
        path = QtWidgets.QFileDialog.getSaveFileName(caption="Export data", filter=tablefilter,
                                                     initialFilter="Excel file (*.xlsx)")
        if path[0] != '':
            workbook = xlsxwriter.Workbook(path[0])
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, "t")
            worksheet.write(0, 1, "vx")
            worksheet.write(0, 2, "vy")
            worksheet.write(0, 3, "v")
            worksheet.write(0, 4, "x")
            worksheet.write(0, 5, "y")
            for row in range(len(self.t)):
                time = self.t[row]
                worksheet.write(row + 1, 0, time)
                worksheet.write(row + 1, 1, self.ux)
                worksheet.write(row + 1, 2, self.uy - self.g * time)
                worksheet.write(row + 1, 3, math.sqrt(self.ux ** 2 + (self.uy - self.g * time) ** 2))
                worksheet.write(row + 1, 4, self.x[row])
                worksheet.write(row + 1, 5, self.y[row])

            workbook.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())