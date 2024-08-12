from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import math
import sys

import numpy as np

import matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import matplotlib.animation as animation

import threading

matplotlib.use('QtAgg')
# plt.rcParams['animation.ffmpeg_path'] = 'C:\\Program Files\\FFMPEG\\ffmpeg-7.0.2-full_build\\bin\\ffmpeg.exe'
Writer = animation.writers['ffmpeg']
writer = Writer(fps=60, metadata=dict(artist='Me'), bitrate=5400)


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

        self.main_font = QFont("Arial", 12)
        self.setFont(self.main_font)

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Challenge #9 by Xingzhi Lu (Concord College)")

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
        self.h_input.setRange(0, 1000000000)
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

        self.inputLayout.addRow(QLabel(''))

        self.cD_input = QDoubleSpinBox()
        self.cD_input.setDecimals(2)
        self.cD_input.setRange(0.01, 1000)
        self.cD_input.setValue(0.1)
        self.cD_input.setSingleStep(0.01)
        self.cD_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('Drag coefficient cD:', self.cD_input)

        self.csa_input = QDoubleSpinBox()
        self.csa_input.setDecimals(6)
        self.csa_input.setRange(0.000001, 10000000)
        self.csa_input.setValue(0.1)
        self.csa_input.setSingleStep(0.01)
        self.csa_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('Cross sectional area (m²):', self.csa_input)

        self.ad_input = QDoubleSpinBox()
        self.ad_input.setDecimals(2)
        self.ad_input.setRange(0.01, 10000000)
        self.ad_input.setValue(1)
        self.ad_input.setSingleStep(1)
        self.ad_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('Air density (kgm⁻³):', self.ad_input)

        self.m_input = QDoubleSpinBox()
        self.m_input.setDecimals(2)
        self.m_input.setRange(0.01, 10000000)
        self.m_input.setValue(0.1)
        self.m_input.setSingleStep(1)
        self.m_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('Object mass (kg):', self.m_input)

        self.inputLayout.addRow(QLabel(''))

        self.dt_input = QDoubleSpinBox()
        self.dt_input.setDecimals(2)
        self.dt_input.setRange(0.01, 0.1)
        self.dt_input.setValue(0.01)
        self.dt_input.setSingleStep(0.01)
        self.dt_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('Time step (s):', self.dt_input)

        self.inputLayout.addRow(QLabel(''))

        self.k_show = QLineEdit()
        self.k_show.setReadOnly(True)
        self.inputLayout.addRow('Air resistance factor k:', self.k_show)

        self.centralLayout.addLayout(self.inputLayout, 0, 0)

        self.graph = MplCanvas(self, width=7, height=5, dpi=100)
        self.graph.tight(2, 0, 0)
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

        cd = self.cD_input.value()
        csa = self.csa_input.value()
        ad = self.ad_input.value()
        m = self.m_input.value()

        dt = self.dt_input.value()

        k = 0.5 * cd * csa * ad / m
        self.k_show.setText(str(round(k, 8)))

        all_x, all_y = [0], [h]

        x, y = 0, h
        vx = u * math.cos(theta_rad)
        vy = u * math.sin(theta_rad)
        v = math.sqrt(vx ** 2 + vy ** 2)

        t = 0

        while y > 0:
            t += dt
            ax = -vx * k * v
            ay = -g - vy * k * v
            x = x + vx * dt + 0.5 * ax * dt ** 2
            y = y + vy * dt + 0.5 * ay * dt ** 2
            vx += ax * dt
            vy += ay * dt
            v = math.sqrt(vx ** 2 + vy ** 2)
            all_x.append(x)
            all_y.append(y)

        self.graph.axes.clear()
        self.graph.axes.plot(all_x, all_y, 'r-', label='With air resistance')

        no_drag_range = u ** 2 / g * (math.sin(theta_rad) * math.cos(theta_rad) + math.cos(theta_rad) * math.sqrt(
            math.sin(theta_rad) ** 2 + 2 * g * h / u ** 2))

        x_values = np.arange(0, no_drag_range, 0.01)
        y_values = h + math.tan(theta_rad) * x_values - 0.5 * g * x_values ** 2 / (u * math.cos(theta_rad)) ** 2

        self.graph.axes.plot(x_values, y_values, 'b-', label='Without air resistance')

        self.graph.axes.set_xlabel('x / m')
        self.graph.axes.set_ylabel('y / m')
        self.graph.axes.set_title('Projectile Motion')
        self.graph.axes.set_xlim(0, no_drag_range * 1.05)
        self.graph.axes.set_ylim(0, max(y_values) * 1.05)

        self.graph.axes.legend()

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
