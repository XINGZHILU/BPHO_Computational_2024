from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import math
import sys

import numpy as np

import matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

from matplotlib.figure import Figure

matplotlib.use('QtAgg')


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        super(MplCanvas, self).__init__(self.fig)

    def tight(self, p, wp, hp):
        self.fig.tight_layout(pad=p, w_pad=wp, h_pad=hp)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mainfont = QFont("Arial", 12)
        self.setFont(self.mainfont)

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Challenge #7")

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.centralLayout = QGridLayout()
        self.central.setLayout(self.centralLayout)

        self.inputLayout = QFormLayout()

        self.titlefont = QFont('Arial', 12)
        self.titlefont.setBold(True)
        self.titlefont.setUnderline(True)

        self.boldfont = QFont('Arial', 12)
        self.boldfont.setBold(True)

        self.inputLabel = QLabel('Inputs:')
        self.inputLabel.setFont(self.titlefont)

        self.inputLayout.addRow(self.inputLabel)

        self.u_input = QDoubleSpinBox()
        self.u_input.setDecimals(2)
        self.u_input.setRange(0.01, 1000000000)
        self.u_input.setValue(10)
        self.u_input.setSingleStep(1)
        self.u_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('u (ms⁻¹):', self.u_input)

        self.g_input = QDoubleSpinBox()
        self.g_input.setDecimals(2)
        self.g_input.setRange(0.01, 1000000000)
        self.g_input.setValue(9.81)
        self.g_input.setSingleStep(0.1)
        self.g_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('g (ms⁻²):', self.g_input)

        self.centralLayout.addLayout(self.inputLayout, 0, 0)

        self.graphs_tab = QTabWidget()
        self.r_tab_widget = QWidget()
        self.r_tab = self.graphs_tab.addTab(self.r_tab_widget, 'Range')
        self.projectile_tab_widget = QWidget()
        self.projectile_tab = self.graphs_tab.addTab(self.projectile_tab_widget, 'Projectile')
        self.graphs_tab.setCurrentIndex(0)
        self.r_tab_Layout = QGridLayout()
        self.projectile_tab_Layout = QGridLayout()

        self.r_graph = MplCanvas(self, width=7, height=5, dpi=100)
        self.r_graph.tight(1.5, 0, 0)
        self.r_tab_Layout.addWidget(self.r_graph, 0, 0, 10, 2)

        self.r_toolbar = NavigationToolbar2QT(self.r_graph, self)
        self.r_tab_Layout.addWidget(self.r_toolbar, 10, 0, 1, 2)

        self.r_tab_widget.setLayout(self.r_tab_Layout)

        self.projectile_graph = MplCanvas(self, width=7, height=5, dpi=100)
        self.projectile_graph.tight(1.5, 0, 0)
        self.projectile_tab_Layout.addWidget(self.projectile_graph, 0, 0, 10, 2)

        self.projectile_toolbar = NavigationToolbar2QT(self.projectile_graph, self)
        self.projectile_tab_Layout.addWidget(self.projectile_toolbar, 10, 0, 1, 2)

        self.projectile_tab_widget.setLayout(self.projectile_tab_Layout)

        self.centralLayout.addWidget(self.graphs_tab, 0, 1, 5, 2)

        self.centralLayout.setColumnStretch(0, 0)
        self.centralLayout.setColumnStretch(1, 1)
        self.centralLayout.setColumnStretch(2, 5)

        self.plot_graph()

    def plot_graph(self):
        self.r_graph.axes.clear()
        self.projectile_graph.axes.clear()
        u = self.u_input.value()
        g = self.g_input.value()
        deg_range_below_70_5 = [30, 45, 60]
        deg_range_over_70_5 = [78, 85]
        self.r_graph.axes.set_title(f'Projectiles: u={self.u_input.value()}ms⁻¹, g={self.g_input.value()}ms⁻²')
        self.r_graph.axes.set_xlabel('t / s')
        self.r_graph.axes.set_ylabel('range r / m')
        max_t = 0
        for deg in [math.radians(i) for i in deg_range_over_70_5]:
            t1 = 3 * u / (2 * g) * (math.sin(deg) - math.sqrt(math.sin(deg) ** 2 - 8 / 9))
            t2 = 3 * u / (2 * g) * (math.sin(deg) + math.sqrt(math.sin(deg) ** 2 - 8 / 9))
            max_t = max(max(t1, t2), max_t)

        t = np.arange(0, max_t * 5, 0.02)
        max_r_graph = 0

        max_y = 0

        for angle in deg_range_below_70_5 + [70.5] + deg_range_over_70_5:
            deg = math.radians(angle)
            r = ((u ** 2) * (t ** 2) - g * (t ** 3) * u * math.sin(deg) + 0.25 * (g ** 2) * (t ** 4)) ** 0.5
            self.r_graph.axes.plot(t, r, label=f'θ={angle}°')

            x_values = u * t * math.cos(deg)
            y_values = u * t * math.sin(deg) - 0.5 * g * t ** 2

            max_y = max(max(y_values), max_y)

            self.projectile_graph.axes.plot(x_values, y_values, label=f'θ={angle}°')

            if angle == 70.5:
                deg = math.radians(70.5)
                t1 = 3 * u / (2 * g) * math.sin(deg)
                r1 = ((u ** 2) * (t1 ** 2) - g * (t1 ** 3) * u * math.sin(deg) + 0.25 * (g ** 2) * (t1 ** 4)) ** 0.5
                self.r_graph.axes.plot(t1, r1, 'rx')
                self.projectile_graph.axes.plot(t1 * u * math.cos(deg), u * t1 * math.sin(deg) - 0.5 * g * t1 ** 2,
                                                'rx')
            elif angle > 70.5:
                t1 = 3 * u / (2 * g) * (math.sin(deg) - math.sqrt(math.sin(deg) ** 2 - 8 / 9))
                t2 = 3 * u / (2 * g) * (math.sin(deg) + math.sqrt(math.sin(deg) ** 2 - 8 / 9))
                r1 = ((u ** 2) * (t1 ** 2) - g * (t1 ** 3) * u * math.sin(deg) + 0.25 * (g ** 2) * (t1 ** 4)) ** 0.5
                r2 = ((u ** 2) * (t2 ** 2) - g * (t2 ** 3) * u * math.sin(deg) + 0.25 * (g ** 2) * (t2 ** 4)) ** 0.5
                self.r_graph.axes.plot(t1, r1, 'rx')
                self.r_graph.axes.plot(t2, r2, 'mx')
                self.projectile_graph.axes.plot(t1 * u * math.cos(deg), u * t1 * math.sin(deg) - 0.5 * g * t1 ** 2,
                                                'rx')
                self.projectile_graph.axes.plot(t2 * u * math.cos(deg), u * t2 * math.sin(deg) - 0.5 * g * t2 ** 2,
                                                'mx')

            max_r_graph = max(r[math.ceil(max_t * 65)], max_r_graph)

        # 70.5 stationary point plotting

        self.r_graph.axes.legend()
        self.projectile_graph.axes.legend()

        self.r_graph.axes.set_xlim(0, max_t * 1.3)
        self.r_graph.axes.set_ylim(0, max_r_graph * 1.1)

        self.projectile_graph.axes.set_xlim(0, u ** 2 / g * 1.05)
        self.projectile_graph.axes.set_ylim(-max_y * 1.05, max_y * 1.05)

        self.r_graph.draw()
        self.projectile_graph.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
