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
        self.setWindowTitle("Challenge #4 by Xingzhi Lu (Concord College)")

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

        self.h_input = QDoubleSpinBox()
        self.h_input.setDecimals(2)
        self.h_input.setRange(0.01, 1000000000)
        self.h_input.setValue(10)
        self.h_input.setSingleStep(1)
        self.h_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('h (m):', self.h_input)

        self.g_input = QDoubleSpinBox()
        self.g_input.setDecimals(2)
        self.g_input.setRange(0.01, 1000000000)
        self.g_input.setValue(9.81)
        self.g_input.setSingleStep(0.1)
        self.g_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('g (ms⁻²):', self.g_input)

        self.deg_input = QDoubleSpinBox()
        self.deg_input.setDecimals(2)
        self.deg_input.setRange(0.01, 89.99)
        self.deg_input.setValue(60)
        self.deg_input.setSingleStep(1)
        self.deg_input.valueChanged.connect(lambda: self.angle_unit_update('deg'))
        self.inputLayout.addRow('θ (degrees):', self.deg_input)

        self.rad_input = QDoubleSpinBox()
        self.rad_input.setDecimals(4)
        self.rad_input.setRange(0.0001, math.pi / 2 - 0.0001)
        self.rad_input.setValue(math.pi / 3)
        self.rad_input.setSingleStep(math.pi / 180)
        self.rad_input.valueChanged.connect(lambda: self.angle_unit_update('rad'))
        self.inputLayout.addRow('θ (radians):', self.rad_input)

        self.centralLayout.addLayout(self.inputLayout, 0, 0)

        self.graph = MplCanvas(self, width=7, height=5, dpi=100)
        self.graph.tight(3, 0, 0)
        self.centralLayout.addWidget(self.graph, 0, 1, 10, 2)

        self.toolbar = NavigationToolbar2QT(self.graph, self)
        self.centralLayout.addWidget(self.toolbar, 10, 1, 1, 2)

        self.centralLayout.setColumnStretch(0, 0)
        self.centralLayout.setColumnStretch(1, 1)
        self.centralLayout.setColumnStretch(2, 5)

        self.plot_graph()

    def plot_graph(self):
        u = self.u_input.value()
        g = self.g_input.value()
        h = self.h_input.value()
        theta_rad = self.rad_input.value()

        input_range = u ** 2 / g * (math.sin(theta_rad) * math.cos(theta_rad) + math.cos(theta_rad) * math.sqrt(
            math.sin(theta_rad) ** 2 + 2 * g * h / u ** 2))
        input_range_time = input_range / (u * math.cos(theta_rad))

        max_range_angle_rad = math.asin(1 / math.sqrt(2 + (2 * g * h) / u ** 2))
        max_range_angle_deg = math.degrees(max_range_angle_rad)
        max_range = u ** 2 / g * math.sqrt(1 + 2 * g * h / u ** 2)
        max_range_time = max_range / (u * math.cos(max_range_angle_rad))

        apogee_y = u ** 2 * math.sin(theta_rad) ** 2 / (2 * g) + h
        apogee_x = u * math.sin(theta_rad) / g

        self.graph.axes.clear()
        self.graph.axes.set_title(
            f'u={u}ms⁻¹, g={g}ms⁻², h={h}m, θ={math.degrees(theta_rad)}°\n (xₐ, yₐ) = ({apogee_x: .2f}m, {apogee_y: .2f}m)')
        self.graph.axes.set_xlabel('x / m')
        self.graph.axes.set_ylabel('y / m')

        t = np.arange(0, max(input_range_time, max_range_time) * 1.01, 0.01)
        y_input = u * t * math.sin(theta_rad) - 0.5 * g * t ** 2 + h
        x_input = u * t * math.cos(theta_rad)
        y_max_range = u * t * math.sin(max_range_angle_rad) - 0.5 * g * t ** 2 + h
        x_max_range = u * t * math.cos(max_range_angle_rad)

        self.graph.axes.plot(x_input, y_input, 'b',
                             label=f'θ = {math.degrees(theta_rad): .2f}°; T={input_range_time: .2f}s; R={input_range: .2f}m')
        self.graph.axes.plot(x_max_range, y_max_range, 'r',
                             label=f'θₘₐₓ = {max_range_angle_deg: .2f}°; T={max_range_time: .2f}s; Rₘₐₓ={max_range: .2f}m')
        self.graph.axes.legend()

        self.graph.axes.set_xlim(0, max_range * 1.05)
        self.graph.axes.set_ylim(0, max(max(y_max_range), max(y_input)) * 1.05)

        self.graph.draw()

    def angle_unit_update(self, changed_input):
        if changed_input == 'deg':
            self.rad_input.setValue(math.radians(self.deg_input.value()))
        else:
            self.deg_input.setValue(math.degrees(self.rad_input.value()))
        self.plot_graph()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
