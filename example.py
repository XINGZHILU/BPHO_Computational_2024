import sys
import matplotlib

import numpy as np

from PyQt6 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from matplotlib.figure import Figure

matplotlib.use('QtAgg')

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

    def p(self):
        print(self.axes)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.plot()
        self.setCentralWidget(central)
        toolbar = NavigationToolbar2QT(self.sc, self)
        layout.addWidget(self.sc)
        layout.addWidget(toolbar)
        central.setLayout(layout)
        self.show()

    def plot(self):
        ux = 10
        t = np.linspace(1, 100, 100)
        x = ux * t
        y = 10 * t - 0.5 * 10 * t * t
        z = t * t
        self.sc.axes.plot(x, y)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()