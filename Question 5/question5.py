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

        self.mainfont = QFont("Arial", 11)
        self.setFont(self.mainfont)

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Challenge #5")

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.centralLayout = QGridLayout()
        self.central.setLayout(self.centralLayout)

        self.inputLayout = QGridLayout()

        self.titlefont = QFont('Arial', 11)
        self.titlefont.setBold(True)
        self.titlefont.setUnderline(True)

        self.boldfont = QFont('Arial', 11)
        self.boldfont.setBold(True)

        self.targetLabel = QLabel('Target (X, Y):')
        self.targetLabel.setFont(self.titlefont)

        self.inputLayout.addWidget(self.targetLabel, 0, 0)

        self.inputLayout.addWidget(QLabel('X (m)'), 1, 0)
        self.inputLayout.addWidget(QLabel('Y (m)'), 2, 0)
        self.X_input = QDoubleSpinBox()
        self.X_input.setMinimum(0)
        self.X_input.setMaximum(10000000000)
        self.X_input.setDecimals(2)
        self.X_input.setValue(1000)
        self.X_input.valueChanged.connect(self.check_min_u)
        self.Y_input = QDoubleSpinBox()
        self.Y_input.setMinimum(0)
        self.Y_input.setMaximum(10000000000)
        self.Y_input.setDecimals(2)
        self.Y_input.setValue(300)
        self.Y_input.valueChanged.connect(self.check_min_u)
        self.inputLayout.addWidget(self.X_input, 1, 1)
        self.inputLayout.addWidget(self.Y_input, 2, 1)

        self.launchLabel = QLabel('\nLaunch settings:')
        self.launchLabel.setFont(self.titlefont)

        self.inputLayout.addWidget(self.launchLabel, 3, 0)
        self.inputLayout.addWidget(QLabel('u (ms⁻¹)'), 4, 0)
        self.inputLayout.addWidget(QLabel('g (ms⁻²)'), 5, 0)

        self.u_input = QDoubleSpinBox()
        self.u_input.setMinimum(0.01)
        self.u_input.setMaximum(10000000000)
        self.u_input.setDecimals(2)
        self.u_input.setSingleStep(0.1)
        self.u_input.setValue(150)
        self.u_input.valueChanged.connect(self.plot_graph)

        self.g_input = QDoubleSpinBox()
        self.g_input.setMinimum(0.01)
        self.g_input.setMaximum(10000000000)
        self.g_input.setDecimals(2)
        self.g_input.setSingleStep(0.1)
        self.g_input.setValue(9.81)
        self.g_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addWidget(self.u_input, 4, 1)
        self.inputLayout.addWidget(self.g_input, 5, 1)

        self.h_input = QDoubleSpinBox()
        self.h_input.setMinimum(0)
        self.h_input.setMaximum(10000000000)
        self.h_input.setDecimals(2)
        self.h_input.setSingleStep(1)
        self.h_input.setValue(0)
        self.h_input.valueChanged.connect(self.plot_graph)
        self.inputLayout.addWidget(QLabel('Initial height (m):'), 6, 0)
        self.inputLayout.addWidget(self.h_input, 6, 1)

        self.inputLayout.addWidget(QLabel('Minimum u (ms⁻¹):'), 7, 0)

        self.min_u_label = QLineEdit()
        self.min_u_label.setReadOnly(True)
        self.inputLayout.addWidget(self.min_u_label, 7, 1)

        self.centralLayout.addLayout(self.inputLayout, 0, 0)

        self.Graph = MplCanvas(self, width=7, height=5, dpi=100)
        self.Graph.tight(1.5, 0, 0)
        self.centralLayout.addWidget(self.Graph, 0, 1, 10, 2)
        self.toolbar = NavigationToolbar2QT(self.Graph, self)
        self.centralLayout.addWidget(self.toolbar, 10, 1, 1, 2)

        self.centralLayout.setColumnStretch(0, 0)
        self.centralLayout.setColumnStretch(1, 1)
        self.centralLayout.setColumnStretch(2, 5)

        self.centralLayout.setRowStretch(0, 0)
        self.centralLayout.setRowStretch(3, 0)

        self.resultLayout = QGridLayout()
        self.centralLayout.addLayout(self.resultLayout, 11, 1)

        self.resultLabel = QLabel('Results:')
        self.resultLabel.setFont(self.titlefont)
        self.resultLayout.addWidget(self.resultLabel, 0, 0)

        self.hb_label_1 = QLabel('High ball angle (rad): ')
        self.hb_label_1.setFont(self.boldfont)
        self.resultLayout.addWidget(self.hb_label_1, 1, 0)
        self.high_ball_angle_Label_rad = QLabel()
        self.resultLayout.addWidget(self.high_ball_angle_Label_rad, 1, 1)
        self.hb_label_2 = QLabel('High ball angle (deg): ')
        self.hb_label_2.setFont(self.boldfont)
        self.resultLayout.addWidget(self.hb_label_2, 1, 2)
        self.high_ball_angle_Label_deg = QLabel()
        self.resultLayout.addWidget(self.high_ball_angle_Label_deg, 1, 3)
        self.hb_label_3 = QLabel('High ball travel time (s): ')
        self.hb_label_3.setFont(self.boldfont)
        self.resultLayout.addWidget(self.hb_label_3, 1, 4)
        self.high_ball_time_Label = QLabel()
        self.resultLayout.addWidget(self.high_ball_time_Label, 1, 5)

        self.lb_label_1 = QLabel('Low ball angle (rad): ')
        self.lb_label_1.setFont(self.boldfont)
        self.resultLayout.addWidget(self.lb_label_1, 2, 0)
        self.low_ball_angle_Label_rad = QLabel()
        self.resultLayout.addWidget(self.low_ball_angle_Label_rad, 2, 1)
        self.lb_label_2 = QLabel('Low ball angle (deg): ')
        self.lb_label_2.setFont(self.boldfont)
        self.resultLayout.addWidget(self.lb_label_2, 2, 2)
        self.low_ball_angle_Label_deg = QLabel()
        self.resultLayout.addWidget(self.low_ball_angle_Label_deg, 2, 3)
        self.lb_label_3 = QLabel('Low ball travel time (s): ')
        self.lb_label_3.setFont(self.boldfont)
        self.resultLayout.addWidget(self.lb_label_3, 2, 4)
        self.low_ball_time_Label = QLabel()
        self.resultLayout.addWidget(self.low_ball_time_Label, 2, 5)

        self.mnu_label_1 = QLabel('Minimum u angle (rad): ')
        self.mnu_label_1.setFont(self.boldfont)
        self.resultLayout.addWidget(self.mnu_label_1, 3, 0)
        self.min_u_angle_Label_rad = QLabel()
        self.resultLayout.addWidget(self.min_u_angle_Label_rad, 3, 1)
        self.mnu_label_2 = QLabel('Minimum u angle (deg): ')
        self.mnu_label_2.setFont(self.boldfont)
        self.resultLayout.addWidget(self.mnu_label_2, 3, 2)
        self.min_u_angle_Label_deg = QLabel()
        self.resultLayout.addWidget(self.min_u_angle_Label_deg, 3, 3)
        self.mnu_label_3 = QLabel('Minimum u travel time (s): ')
        self.mnu_label_3.setFont(self.boldfont)
        self.resultLayout.addWidget(self.mnu_label_3, 3, 4)
        self.min_u_time_Label = QLabel()
        self.resultLayout.addWidget(self.min_u_time_Label, 3, 5)

        self.check_min_u()

    def check_min_u(self):
        self.min_u = math.sqrt(self.g_input.value()) * math.sqrt(
            self.Y_input.value() + math.sqrt(self.X_input.value() ** 2 + self.Y_input.value() ** 2))
        self.min_u_label.setText(str(self.min_u))
        self.u_input.setMinimum(self.min_u)
        self.plot_graph()

    def plot_graph(self):
        Y = self.Y_input.value()
        X = self.X_input.value()
        u = self.u_input.value()
        g = self.g_input.value()
        h = self.h_input.value()

        actual_Y = Y - h

        a = g / (2 * u ** 2) * X ** 2
        b = -X
        c = actual_Y + g / (2 * u ** 2) * X ** 2

        low_angle = math.atan((-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a))
        high_angle = math.atan((-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a))
        min_u_angle = math.atan((actual_Y + math.sqrt(X ** 2 + actual_Y ** 2)) / X)

        self.high_ball_angle_Label_rad.setText(str(round(high_angle, 4)))
        self.high_ball_angle_Label_deg.setText(str(round(math.degrees(high_angle), 2)))
        self.low_ball_angle_Label_rad.setText(str(round(low_angle, 4)))
        self.low_ball_angle_Label_deg.setText(str(round(math.degrees(low_angle), 2)))
        self.min_u_angle_Label_rad.setText(str(round(min_u_angle, 4)))
        self.min_u_angle_Label_deg.setText(str(round(math.degrees(min_u_angle), 2)))

        self.high_ball_time_Label.setText(str(round(X / (u * math.cos(high_angle)), 2)))
        self.low_ball_time_Label.setText(str(round(X / (u * math.cos(low_angle)), 2)))
        self.min_u_time_Label.setText(str(round(X / (self.min_u * math.cos(min_u_angle)), 2)))

        self.Graph.axes.clear()
        self.Graph.axes.set_title(f'Projectile through ({X}, {Y}), u={u}ms⁻¹, g={g}ms⁻², h={h}m')
        self.Graph.axes.set_xlabel('x / m')
        self.Graph.axes.set_ylabel('y / m')

        x_values = np.arange(0, X, 0.01)
        x_values_more = np.arange(0, X * 1.2, 0.1)

        min_u_y_values = ((actual_Y + math.sqrt(X ** 2 + actual_Y ** 2)) / X) * x_values - (
                math.sqrt(X ** 2 + actual_Y ** 2) / (X ** 2)) * x_values ** 2 + h
        bounding_y_values = u ** 2 / (2 * g) - (g / (2 * u ** 2)) * x_values_more ** 2 + h
        high_y_values = math.tan(high_angle) * x_values - (g / (2 * u ** 2)) * (
                1 + math.tan(high_angle) ** 2) * x_values ** 2 + h
        low_y_values = math.tan(low_angle) * x_values - (g / (2 * u ** 2)) * (
                1 + math.tan(low_angle) ** 2) * x_values ** 2 + h

        self.Graph.axes.plot(x_values, min_u_y_values, 'b-', label='Min u')
        self.Graph.axes.plot(x_values, high_y_values, 'g-', label='High angle')
        self.Graph.axes.plot(x_values, low_y_values, 'c-', label='Low angle')
        self.Graph.axes.plot(x_values_more, bounding_y_values, 'r-', label='Bounding parabola')

        self.Graph.axes.plot(X, Y, 'rx', label=f'Target ({X}, {Y})')
        self.Graph.axes.plot(0, h, 'm*', label=f'Launch (0, {h})')

        self.Graph.axes.set_xlim(0, X * 1.01)
        self.Graph.axes.set_ylim(0, (u ** 2 / (2 * g) + h) * 1.1)

        self.Graph.axes.legend()

        self.Graph.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
