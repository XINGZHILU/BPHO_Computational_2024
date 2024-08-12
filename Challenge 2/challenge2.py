import pathlib

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

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


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Ui_Table(object):
    def setupUi(self, Table, x, y, len):
        Table.setObjectName("Table")
        Table.resize(450, 450)
        self.verticalLayout = QVBoxLayout()
        Table.setLayout(self.verticalLayout)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.DataTable = QTableWidget()
        self.DataTable.setObjectName("DataTable")
        self.DataTable.setColumnCount(2)
        self.DataTable.setRowCount(0)
        item = QTableWidgetItem()
        self.DataTable.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.DataTable.setHorizontalHeaderItem(1, item)
        self.DataTable.setColumnWidth(0, 200)
        self.DataTable.setColumnWidth(1, 200)

        self.verticalLayout.addWidget(self.DataTable)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setEnabled(True)
        self.buttonBox.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedKingdom))
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.clicked.connect(Table.reject)

        self.retranslateUi(Table)
        QMetaObject.connectSlotsByName(Table)
        self.table(x, y, len)

    def retranslateUi(self, Table):
        _translate = QCoreApplication.translate
        Table.setWindowTitle(_translate("Table", "Data"))
        Table.setWindowIcon(QIcon(resource_path("img/Mainicon.png")))
        item = self.DataTable.horizontalHeaderItem(0)
        item.setText(_translate("Table", "x"))
        item = self.DataTable.horizontalHeaderItem(1)
        item.setText(_translate("Table", "y"))

    def table(self, x, y, len):
        self.DataTable.setRowCount(len)
        for row in range(len):
            self.DataTable.setItem(row, 0, QTableWidgetItem(str(x[row])))
            self.DataTable.setItem(row, 1, QTableWidgetItem(str(y[row])))
        self.delegate = ReadOnlyDelegate()
        self.DataTable.setItemDelegate(self.delegate)


class Ui_Settings(object):
    def setupUi(self, Settings, parent, fraction, col):
        self.parent = parent
        self.col = col
        Settings.setObjectName("Settings")
        Settings.resize(400, 100)
        self.gridLayoutWidget = QWidget(parent=Settings)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")
        Settings.setLayout(self.gridLayout)
        self.buttonBox = QDialogButtonBox(parent=self.gridLayoutWidget)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.mainLayout = QFormLayout()
        self.mainLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.mainLayout.setObjectName("mainLayout")
        self.fractionervalLabel = QLabel(parent=self.gridLayoutWidget)
        self.fractionervalLabel.setObjectName("tIntervalLabel")
        self.mainLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.fractionervalLabel)
        self.graphColourLabel = QLabel(parent=self.gridLayoutWidget)
        self.graphColourLabel.setObjectName("graphColourLabel")
        self.mainLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.graphColourLabel)
        self.fractionSpinbox = QSpinBox(parent=self.gridLayoutWidget)
        self.fractionSpinbox.setObjectName("fractionSpinbox")
        self.fractionSpinbox.setSingleStep(10)
        self.fractionSpinbox.setRange(10, 10000000)
        self.fractionSpinbox.setValue(fraction)
        self.fractionSpinbox.valueChanged.connect(self.change)
        self.mainLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.fractionSpinbox)
        self.comboBox = QComboBox(parent=self.gridLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(['Blue', 'Green', 'Red', 'Cyan', 'Purple', 'Yellow', 'Black', 'White'])
        self.comboBox.setCurrentIndex(col)
        self.comboBox.currentIndexChanged.connect(self.change)
        self.mainLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.comboBox)
        self.gridLayout.addLayout(self.mainLayout, 0, 0, 1, 1)

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)  # type: ignore
        self.buttonBox.rejected.connect(Settings.reject)  # type: ignore
        QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        Settings.setWindowIcon(QIcon(resource_path("img/Mainicon.png")))
        self.fractionervalLabel.setText(_translate("Settings", "Number of fractions"))
        self.graphColourLabel.setText(_translate("Settings", "Graph colour"))
        self.comboBox.setCurrentIndex(self.col)

    def change(self):
        self.parent.newfrac = self.fractionSpinbox.value()
        self.parent.newcol = self.comboBox.currentIndex()


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        super(MplCanvas, self).__init__(self.fig)

    def tight(self, p, wp, hp):
        self.fig.tight_layout(pad=p, w_pad=wp, h_pad=hp)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.changed = False
        self.readjson()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily("Arial")
        font.setPixelSize(14)
        MainWindow.setFont(font)
        MainWindow.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedKingdom))
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonFollowStyle)
        self.centralwidget = QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainLayoutWidget = QWidget(parent=self.centralwidget)
        self.mainLayoutWidget.setObjectName("mainLayoutWidget")
        self.mainLayout = QGridLayout(self.mainLayoutWidget)
        self.mainLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setObjectName("mainLayout")
        self.inputLayout = QFormLayout()
        self.inputLayout.setObjectName("inputLayout")
        self.launchAngleDegreeLabel = QLabel(parent=self.mainLayoutWidget)
        self.launchAngleDegreeLabel.setObjectName("launchAngleDegreeLabel")
        self.inputLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.launchAngleDegreeLabel)
        self.launchAngelRadianLabel = QLabel(parent=self.mainLayoutWidget)
        self.launchAngelRadianLabel.setObjectName("launchAngelRadianLabel")
        self.inputLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.launchAngelRadianLabel)
        self.RadSpinbox = QDoubleSpinBox(parent=self.mainLayoutWidget)
        self.RadSpinbox.setDecimals(12)
        self.RadSpinbox.setRange(0, math.pi / 2)
        self.RadSpinbox.setValue(math.pi / 4)
        self.RadSpinbox.setSingleStep(math.pi / 180)
        self.RadSpinbox.valueChanged.connect(self.radtodeg)
        self.inputLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.RadSpinbox)
        self.launchSpeedMs1Label = QLabel(parent=self.mainLayoutWidget)
        self.launchSpeedMs1Label.setObjectName("launchSpeedMs1Label")
        self.inputLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.launchSpeedMs1Label)
        self.launchHeightMLabel = QLabel(parent=self.mainLayoutWidget)
        self.launchHeightMLabel.setObjectName("launchHeightMLabel")
        self.inputLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.launchHeightMLabel)
        self.gMs2Label = QLabel(parent=self.mainLayoutWidget)
        self.gMs2Label.setObjectName("gMs2Label")
        self.inputLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.gMs2Label)
        self.GSpinBox = QDoubleSpinBox(parent=self.mainLayoutWidget)
        self.GSpinBox.setMaximum(9999999999.0)
        self.GSpinBox.setSingleStep(0.1)
        self.GSpinBox.setProperty("value", 9.81)
        self.GSpinBox.setObjectName("GSpinBox")
        self.GSpinBox.valueChanged.connect(self.updategraph)
        self.GSpinBox.setRange(0, 99999999)
        self.inputLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.GSpinBox)
        self.DegSpinbox = QDoubleSpinBox(parent=self.mainLayoutWidget)
        self.DegSpinbox.setDecimals(2)
        self.DegSpinbox.setValue(45)
        self.DegSpinbox.setRange(0, 90)
        self.DegSpinbox.setSingleStep(1.0)
        self.DegSpinbox.valueChanged.connect(self.degtorad)
        self.inputLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.DegSpinbox)
        self.SpeedSpinBox = QDoubleSpinBox(parent=self.mainLayoutWidget)
        self.SpeedSpinBox.setSingleStep(1)
        self.SpeedSpinBox.setProperty("value", 10.0)
        self.SpeedSpinBox.setObjectName("SpeedSpinBox")
        self.SpeedSpinBox.valueChanged.connect(self.updategraph)
        self.SpeedSpinBox.setRange(0, 99999999)
        self.inputLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.SpeedSpinBox)
        self.HeightSpinBox = QDoubleSpinBox(parent=self.mainLayoutWidget)
        self.HeightSpinBox.setProperty("value", 10.0)
        self.HeightSpinBox.setObjectName("HeightSpinBox")
        self.HeightSpinBox.valueChanged.connect(self.updategraph)
        self.HeightSpinBox.setRange(0, 99999999)

        self.inputLayout.addRow("", QLabel())

        self.RShow = QLineEdit()
        self.RShow.setReadOnly(True)
        self.inputLayout.addRow("Range R (m)", self.RShow)

        self.xaShow = QLineEdit()
        self.xaShow.setReadOnly(True)
        self.inputLayout.addRow("Apogee xa (m)", self.xaShow)

        self.yaShow = QLineEdit()
        self.yaShow.setReadOnly(True)
        self.inputLayout.addRow("Apogee ya (m)", self.yaShow)

        self.TShow = QLineEdit()
        self.TShow.setReadOnly(True)
        self.inputLayout.addRow("Time of flight T (s)", self.TShow)

        self.inputLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.HeightSpinBox)
        self.mainLayout.addLayout(self.inputLayout, 0, 0, 1, 1)

        self.Graph = MplCanvas(self, width=7, height=5, dpi=100)
        self.Graph.setObjectName("Graph")
        self.Graph.tight(1.5, 0, 0)
        self.mainLayout.addWidget(self.Graph, 0, 1, 2, 1)
        toolbar = NavigationToolbar2QT(self.Graph, MainWindow)
        self.mainLayout.addWidget(toolbar, 2, 1, 3, 1)
        self.mainLayout.setColumnMinimumWidth(0, 320)
        self.mainLayout.setColumnStretch(1, 3)
        self.mainLayout.setRowStretch(1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menuData = QMenu(parent=self.menubar)
        self.menuData.setObjectName("menuData")
        self.menuOptions = QMenu(parent=self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionShow_data = QAction("Show data")
        self.actionShow_data.setObjectName("actionShow_data")
        self.actionExport_data = QAction(parent=MainWindow)
        self.actionExport_data.setObjectName("actionExport_data")
        self.actionSettings = QAction(parent=MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.menuData.addAction(self.actionShow_data)
        self.menuData.addAction(self.actionExport_data)
        self.menuOptions.addAction(self.actionSettings)
        self.menubar.addAction(self.menuData.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        self.centralwidget.setLayout(self.mainLayout)

        self.updategraph()

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Challenge #2 by Xingzhi Lu (Concord College)"))
        MainWindow.setWindowIcon(QIcon(resource_path("img/Mainicon.png")))
        self.launchAngleDegreeLabel.setText(_translate("MainWindow", "Launch angle (degree)"))
        self.launchAngelRadianLabel.setText(_translate("MainWindow", "Launch angle (radian)"))
        self.launchSpeedMs1Label.setText(_translate("MainWindow", "Launch speed (ms⁻¹)"))
        self.launchHeightMLabel.setText(_translate("MainWindow", "Launch height (m)"))
        self.gMs2Label.setText(_translate("MainWindow", "g (ms⁻²)"))
        self.menuData.setTitle(_translate("MainWindow", "Data"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.actionShow_data.setText(_translate("MainWindow", "Show data table"))
        self.actionShow_data.setShortcut("Ctrl+T")
        self.actionShow_data.setIcon(QIcon(resource_path("img/Table.png")))
        self.actionShow_data.triggered.connect(self.showtable)
        self.actionExport_data.setText(_translate("MainWindow", "Export data"))
        self.actionExport_data.setShortcut("Ctrl+E")
        self.actionExport_data.setIcon(QIcon(resource_path("img/Export.png")))
        self.actionExport_data.triggered.connect(self.exporttable)
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionSettings.triggered.connect(self.asksettings)
        self.actionSettings.setIcon(QIcon(resource_path("img/Settings.png")))
        self.actionSettings.setShortcut("Ctrl+Shift+S")

    def asksettings(self):  # startup another dialog
        self.newfrac = 100
        self.newcol = 0
        Dialog = QDialog()
        ui = Ui_Settings()
        ui.setupUi(Dialog, self, self.fraction, self.col)
        if Dialog.exec():  # check if OK is pressed
            self.fraction = self.newfrac
            self.col = self.newcol
            f = open(self.jsondir, 'w')
            json.dump({'fractions': self.fraction, 'GraphColour': self.col}, f)
            f.close()
            self.updategraph()

    def readjson(self):  # read from settings.json for self.fraction and self.col
        docdir = str(pathlib.Path.home()) + '/Documents'
        self.jsondir = f"{docdir}/BPHO/settings_2.json"
        if not os.path.exists(docdir + '/BPHO'):
            os.mkdir(docdir + '/BPHO')
        try:
            f = open(self.jsondir, 'r')
            data = json.load(f)
            f.close()
            self.fraction = data['fractions']
            self.col = data['GraphColour']
        except FileNotFoundError:
            data = {'fractions': 100, 'GraphColour': 0}
            f = open(self.jsondir, 'w')
            json.dump(data, f)
            f.close()
            self.fraction = 100
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
        self.u = self.SpeedSpinBox.value()
        self.theta = self.RadSpinbox.value()
        self.h = self.HeightSpinBox.value()
        self.g = self.GSpinBox.value()
        self.R = self.u * self.u / self.g * (
                    math.sin(self.theta) * math.cos(self.theta) + math.cos(self.theta) * math.sqrt(
                math.sin(self.theta) ** 2 + 2 * self.g * self.h / (self.u ** 2)))
        self.x = np.linspace(0, self.R, self.fraction)
        self.y = self.h + self.x * math.tan(self.theta) - (self.g / 2 / self.u / self.u) * (
                    1 + math.tan(self.theta) ** 2) * (self.x * self.x)
        self.xa = self.u ** 2 / self.g * math.sin(self.theta) * math.cos(self.theta)
        self.ya = self.h + self.u ** 2 / self.g / 2 * math.sin(self.theta) ** 2
        self.T = self.R / self.u / math.cos(self.theta)
        self.Graph.axes.plot(self.x, self.y, color='bgrcmykw'[self.col], marker=".", label="y vs x")
        self.Graph.axes.plot(self.xa, self.ya, 'x', color='r', label="apogee")
        self.Graph.axes.set_xlim(0, self.R * 1.1)
        self.Graph.axes.set_ylim(0, self.ya * 1.1)
        self.Graph.axes.set_title("Projectile motion model - with air resistance")
        self.Graph.axes.set_xlabel("x / m")
        self.Graph.axes.set_ylabel("y / m")
        self.Graph.axes.grid()
        self.Graph.axes.legend()
        self.Graph.draw()

        # update display boxes
        self.RShow.setText(str(round(self.R, 2)))
        self.xaShow.setText(str(round(self.xa, 2)))
        self.yaShow.setText(str(round(self.ya, 2)))
        self.TShow.setText(str(round(self.T, 2)))

    def showtable(self):
        Dialog = QDialog()
        ui = Ui_Table()
        ui.setupUi(Dialog, self.x, self.y, self.fraction)
        Dialog.exec()

    def exporttable(self):
        tablefilter = "Excel file (*.xlsx)"
        path = QFileDialog.getSaveFileName(caption="Export data", filter=tablefilter,
                                           initialFilter="Excel file (*.xlsx)")
        if path[0] != '':
            workbook = xlsxwriter.Workbook(path[0])
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, "x")
            worksheet.write(0, 1, "y")
            for row in range(self.fraction):
                worksheet.write(row + 1, 0, self.x[row])
                worksheet.write(row + 1, 1, self.y[row])

            self.close = workbook.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
