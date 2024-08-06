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

        self.update_count = 0

        self.dt = 0.02

        self.started = False
        self.first_draw_finished = False
        self.drawing = 0

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Challenge #8 by Xingzhi Lu (Concord College)")

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
        self.c_input.setValue(0.7)
        self.c_input.setSingleStep(0.01)
        self.c_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('c:', self.c_input)

        self.nbounce_input = QSpinBox()
        self.nbounce_input.setRange(0, 100)
        self.nbounce_input.setValue(1)
        self.nbounce_input.setSingleStep(1)
        self.nbounce_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addRow('Number of bounces simulated:', self.nbounce_input)

        self.inputs = [self.u_input, self.h_input, self.g_input, self.deg_input, self.rad_input, self.c_input,
                       self.nbounce_input]

        self.submit_button = QPushButton('Restart animation')
        self.submit_button.clicked.connect(self.plot_graph)
        self.inputLayout.addRow(QLabel(''))
        self.inputLayout.addRow(self.submit_button)

        self.skip_button = QPushButton('Skip to end')
        self.skip_button.clicked.connect(self.skip_animation)
        self.inputLayout.addRow(self.skip_button)

        self.centralLayout.addLayout(self.inputLayout, 0, 0)

        self.graph = MplCanvas(self, width=7, height=5, dpi=100)
        self.graph.tight(3, 0, 0)
        self.centralLayout.addWidget(self.graph, 0, 1, 10, 2)

        self.toolbar = NavigationToolbar2QT(self.graph, self)
        self.centralLayout.addWidget(self.toolbar, 10, 1, 1, 2)

        self.export_button = QPushButton('Export Video')
        self.export_button.clicked.connect(self.export_video)
        self.centralLayout.addWidget(self.export_button, 11, 1, 1, 2)

        self.centralLayout.setColumnStretch(0, 0)
        self.centralLayout.setColumnStretch(1, 1)
        self.centralLayout.setColumnStretch(2, 5)

        self.plot_graph()

    def plot_graph(self):
        if self.first_draw_finished:
            self.graph.callbacks.process('close_event')
            self.graph.deleteLater()
            self.centralLayout.removeWidget(self.graph)
            self.graph = MplCanvas(self, width=7, height=5, dpi=100)
            self.graph.tight(3, 0, 0)
            self.centralLayout.addWidget(self.graph, 0, 1, 10, 2)

        
        
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

        # calculate all the points

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

        for i in range(10):
            self.all_x.append(self.all_x[-1])
            self.all_y.append(self.all_y[-1])
            self.all_t.append(self.all_t[-1])

        self.graph.axes.clear()

        self.max_x, self.max_y = max(self.all_x), max(self.all_y)

        self.ball, = self.graph.axes.plot(self.x, self.y, 'ro')
        self.track, = self.graph.axes.plot(self.x, self.y, 'r-')

        self.graph.axes.set_xlabel('X (m)')
        self.graph.axes.set_ylabel('Y (m)')

        self.graph.axes.set_xlim(0, self.max_x * 1.05)
        self.graph.axes.set_ylim(0, self.max_y * 1.05)

        self.projectile_animation = animation.FuncAnimation(fig=self.graph.fig, func=self.ani, frames=len(self.all_t),
                                                            interval=20, repeat=False)

        self.projectile_animation.pause()
        self.projectile_animation.resume()

        self.first_draw_finished = True
        self.drawing += 1



    def ani(self, frame):
        self.ball.set_xdata([self.all_x[frame]])
        self.ball.set_ydata([self.all_y[frame]])

        self.track.set_xdata(self.all_x[:frame + 1])
        self.track.set_ydata(self.all_y[:frame + 1])

        self.graph.axes.set_xlim(0, self.max_x * 1.05)
        self.graph.axes.set_ylim(0, self.max_y * 1.05)

        self.graph.axes.set_title(f't={self.all_t[frame]:.2f}s')

    def angle_unit_update(self, changed_input):
        if changed_input == 'deg':
            self.rad_input.setValue(math.radians(self.deg_input.value()))
        else:
            self.deg_input.setValue(math.degrees(self.rad_input.value()))
        self.plot_graph()

    def export_video(self):
        save_location = QFileDialog.getSaveFileName(self, 'Save Video', '', 'MP4 Files (*.mp4)')
        if save_location[0]:
            save_thread = threading.Thread(target=lambda: self.save_video(save_location[0]))
            save_thread.start()

    def save_video(self, path):
        self.export_fig = plt.figure()
        self.export_ball, = plt.plot(0, self.h, 'ro')
        self.export_track, = plt.plot(0, self.h, 'r-')
        plt.xlabel('X (m)')
        plt.ylabel('Y (m)')
        projectile_ani = animation.FuncAnimation(self.export_fig, self.export_ani, frames=len(self.all_t), interval=20,
                                                 blit=True)
        projectile_ani.save(path, writer=writer)

    def export_ani(self, frame):
        self.export_ball.set_xdata([self.all_x[frame]])
        self.export_ball.set_ydata([self.all_y[frame]])

        self.export_track.set_xdata(self.all_x[:frame + 1])
        self.export_track.set_ydata(self.all_y[:frame + 1])

        plt.xlim(0, self.max_x * 1.05)
        plt.ylim(0, self.max_y * 1.05)

        self.export_fig.suptitle(f't={self.all_t[frame]:.2f}s')

        return self.export_ball, self.export_track

    def skip_animation(self):
        self.projectile_animation.pause()
        self.graph.axes.clear()
        self.ball, = self.graph.axes.plot(self.all_x[-1], self.all_y[-1], 'ro')
        self.track, = self.graph.axes.plot(self.all_x, self.all_y, 'r-')
        self.graph.axes.set_xlabel('X (m)')
        self.graph.axes.set_ylabel('Y (m)')
        self.graph.axes.set_title(f't={self.all_t[-1]:.2f}s')
        self.graph.axes.set_xlim(0, self.max_x * 1.05)
        self.graph.axes.set_ylim(0, self.max_y * 1.05)
        self.graph.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
