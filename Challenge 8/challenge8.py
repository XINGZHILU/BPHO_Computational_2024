from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import math
import sys

import numpy as np

import matplotlib

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

from matplotlib.figure import Figure

import matplotlib.animation as animation

import threading

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

        self.main_font = QFont("Arial", 12)
        self.setFont(self.main_font)

        self.update_count = 0

        self.dt = 0.02

        self.started = False
        self.first_draw_finished = False

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Challenge #4")

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

        self.c_input = QDoubleSpinBox()
        self.c_input.setDecimals(2)
        self.c_input.setRange(0.01, 1)
        self.c_input.setValue(0.5)
        self.c_input.setSingleStep(0.01)
        self.c_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('c:', self.c_input)

        self.nbounce_input = QSpinBox()
        self.nbounce_input.setRange(0, 100)
        self.nbounce_input.setValue(1)
        self.nbounce_input.setSingleStep(1)
        self.nbounce_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('Number of bounces simulated:', self.nbounce_input)

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
        if self.first_draw_finished:
            self.projectile_animation.event_source.stop()
        self.u = self.u_input.value()
        self.g = self.g_input.value()
        self.h = self.h_input.value()
        self.theta_rad = self.rad_input.value()
        self.c = self.c_input.value()
        self.max_n = self.nbounce_input.value()

        self.t = 0

        self.nbounce = 0

        self.x, self.y = 0, self.h
        self.ax, self.ay = 0, -self.g
        self.vx = self.u * math.cos(self.theta_rad)
        self.vy = self.u * math.sin(self.theta_rad)
        self.all_x, self.all_y = [self.x], [self.y]
        self.all_t = [self.t]

        self.frame_no = 1

        while self.nbounce <= self.max_n:
            self.t += self.dt
            self.x = self.x + self.vx * self.dt + 0.5 * self.ax * self.dt ** 2
            self.y = self.y + self.vy * self.dt + 0.5 * self.ay * self.dt ** 2


            aax, aay = 0, -self.g

            self.vx = self.vx + 0.5 * (self.ax + aax) * self.dt
            self.vy = self.vy + 0.5 * (self.ay + aay) * self.dt

            if self.y < 0:
                self.nbounce += 1
                self.y = 0
                self.vy = -self.vy * self.c

            self.all_x.append(self.x)
            self.all_y.append(self.y)

            self.all_t.append(self.t)

            self.frame_no += 1

        self.graph.axes.clear()

        self.ball, = self.graph.axes.plot(self.x, self.y, 'ro')
        self.track, = self.graph.axes.plot(self.all_x, self.all_y, 'r-')

        self.graph.draw()

        self.projectile_animation = animation.FuncAnimation(fig=self.graph.fig, func=self.ani, frames=None, interval=20,
                                                            cache_frame_data=False)
        self.first_draw_finished = True



    def ani(self, frame):
        if self.nbounce <= self.max_n:
            self.t += self.dt
            self.x = self.x + self.vx * self.dt + 0.5 * self.ax * self.dt ** 2
            self.y = self.y + self.vy * self.dt + 0.5 * self.ay * self.dt ** 2


            aax, aay = 0, -self.g

            self.vx = self.vx + 0.5 * (self.ax + aax) * self.dt
            self.vy = self.vy + 0.5 * (self.ay + aay) * self.dt

            if self.y < 0:
                self.nbounce += 1
                self.y = 0
                self.vy = -self.vy * self.c

            self.all_x.append(self.x)
            self.all_y.append(self.y)

            self.ball.set_xdata(self.all_x[-1])
            self.ball.set_ydata([self.y])

            self.track.set_xdata(self.all_x)
            self.track.set_ydata(self.all_y)

            self.graph.axes.set_xlim(0, 50)
            self.graph.axes.set_ylim(0, self.h_input.value() * 2)

            self.graph.axes.set_title(f't={self.t:.2f}s')
        else:
            try:
                self.projectile_animation.save('first_animation.mp4', fps=50, extra_args=['-vcodec', 'libx264'])
            except:
                print('Error saving')
            self.projectile_animation.event_source.stop()

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
