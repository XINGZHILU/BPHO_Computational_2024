import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.pylab as pylab
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os

matplotlib.use('QtAgg')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, width=5, height=4, dpi=100):
        self.fig = plt.figure(figsize=(5,4))
        self.ax = self.fig.add_subplot(111,projection='3d')
        super(MplCanvas, self).__init__(self.fig)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.sysfont = QFont('Arial', 9)
        '''
        self.central = QTabWidget()

        self.inner = MplCanvas()
        self.central.addTab(self.inner, 'Inner Planets')

        self.outer = MplCanvas()
        self.central.addTab(self.outer,'Outer Planets and Pluto')
        '''

        self.central = QWidget()
        self.centrallayout = QGridLayout()

        self.inner = MplCanvas()
        self.centrallayout.addWidget(self.inner,0,0)

        self.outer = MplCanvas()
        self.centrallayout.addWidget(self.outer,0,1)

        self.central.setLayout(self.centrallayout)

        self.setCentralWidget(self.central)
        self.setWindowTitle('Challenge 4')

        self.active = False
        self.stateicon = [QIcon(resource_path('Start128.ico')), QIcon(resource_path('Pause128.ico'))]
        self.pause_action = QAction('Pause', self)
        self.file_toolbar = self.addToolBar('Toolbar')
        self.file_toolbar.addAction(self.pause_action)
        self.pause_action.setIcon(self.stateicon[self.active])
        self.pause_action.setShortcut('Space')
        self.pause_action.setToolTip('tool')
        self.pause_action.setStatusTip('status')
        self.pause_action.triggered.connect(self.pause)

        self.plotinner()
        self.plotouter()
        self.setFont(self.sysfont)

    def plotouter(self):
        self.outer.ax.set(xbound = [-40,60], ybound = [-40,40], zbound = [-20,20],
                          xlabel = 'x/AU', ylabel = 'y/AU', zlabel = 'z/AU')
        self.outer.ax.set_autoscale_on(False)
        self.outer.ax.set_aspect('equal')
        obj = ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
        outereccentricity = [0.05, 0.06, 0.05, 0.01, 0.25]
        self.outera = [5.202, 9.576, 19.293, 30.246, 39.509]
        self.outerP = [11.861, 29.628, 84.747, 166.344, 248.348]
        self.outert = 0
        self.outerB = [1.31,2.49,0.77,1.77,17.5]
        self.outerB = [B/180*math.pi for B in self.outerB]
        colours = 'cmykb'

        deg = np.linspace(0, 2 * math.pi, 1000)
        cosine = np.array([math.cos(i) for i in deg])
        sine = np.array([math.sin(i) for i in deg])
        self.jupiter = self.outer.ax.plot(0, 0, 0, 'co')[0]
        self.saturn = self.outer.ax.plot(0, 0, 0, 'mo')[0]
        self.uranus = self.outer.ax.plot(0, 0, 0, 'yo')[0]
        self.neptune = self.outer.ax.plot(0, 0, 0, 'ko')[0]
        self.pluto = self.outer.ax.plot(0, 0, 0, 'bo')[0]
        self.outer_planets = [self.jupiter, self.saturn, self.uranus, self.neptune, self.pluto]
        self.outer.ax.plot(0, 0, 0, 'ro', label='Sun')
        self.outerpos = []
        for i in range(len(obj)):
            r = self.outera[i] * (1 - outereccentricity[i] ** 2) / (1 - outereccentricity[i] * cosine)
            x = [r[i] * cosine[i] for i in range(1000)]
            y = [r[i] * sine[i] for i in range(1000)]
            z = [x0 * math.sin(self.outerB[i]) for x0 in x]
            self.outer.ax.plot(x, y, z, colours[i], label=obj[i])
            self.outerpos.append([x,y,z])

        self.outer.ax.legend()
        self.outer.ax.grid(True)
        self.outer.ax.set_title('Outer Planets and Pluto')

        self.outerani = animation.FuncAnimation(fig=self.outer.fig, func=self.ani_outer, frames=None, interval=20,
                                                cache_frame_data=False)

    def ani_outer(self, frame):
        if self.active:
            inc = 11.861 / 50
            for i in range(5):
                progress = (self.outert / self.outerP[i]) % 1
                pos = min(int(round(1000 * progress)), 999)
                self.outer_planets[i].set_xdata([self.outerpos[i][0][pos]])
                self.outer_planets[i].set_ydata([self.outerpos[i][1][pos]])
                self.outer_planets[i].set_3d_properties([self.outerpos[i][2][pos]])
            self.outert += inc
            return (self.jupiter, self.saturn, self.uranus, self.neptune)

    def plotinner(self):
        self.inner.ax.set(xbound = [-1.6,1.8], ybound = [-1.6,1.6], zbound = [-1,1],
                          xlabel = 'x/AU', ylabel = 'y/AU', zlabel = 'z/AU')
        self.inner.ax.set_autoscale_on(False)
        self.inner.ax.set_aspect('equal')
        obj = ['Mercury', 'Venus', 'Earth', 'Mars']
        innereccentricity = [0.21, 0.01, 0.02, 0.09]
        self.innera = [0.387, 0.723, 1, 1.523]
        self.innerP = [0.241, 0.615, 1, 1.881]
        self.innert = 0
        self.innerB = [7.00,3.39,0,1.85]
        self.innerB = [B/180*math.pi for B in self.innerB]
        colours = 'cmykb'

        deg = np.linspace(0, 2 * math.pi, 1000)
        cosine = np.array([math.cos(i) for i in deg])
        sine = np.array([math.sin(i) for i in deg])
        self.mercury = self.inner.ax.plot(0, 0, 0, 'co')[0]
        self.venus = self.inner.ax.plot(0, 0, 'mo')[0]
        self.earth = self.inner.ax.plot(0, 0, 'yo')[0]
        self.mars = self.inner.ax.plot(0, 0, 'ko')[0]
        self.inner_planets = [self.mercury, self.venus, self.earth, self.mars]
        self.inner.ax.plot(0, 0, 0, 'ro', label='Sun')
        self.innerpos = []
        for i in range(len(obj)):
            r = self.innera[i] * (1 - innereccentricity[i] ** 2) / (1 - innereccentricity[i] * cosine)
            x = [r[i] * cosine[i] for i in range(1000)]
            y = [r[i] * sine[i] for i in range(1000)]
            z = [x0 * math.sin(self.innerB[i]) for x0 in x]
            self.inner.ax.plot(x, y, z, colours[i], label=obj[i])
            self.innerpos.append([x,y,z])
        self.inner.ax.legend()
        self.inner.ax.grid(True)
        self.inner.ax.set_title('Inner Planets')

        self.innerani = animation.FuncAnimation(fig=self.inner.fig, func=self.ani_inner, frames=None, interval=20,
                                                cache_frame_data=False)

    def ani_inner(self, frame):
        if self.active:
            inc = 0.02
            for i in range(4):
                progress = (self.innert / self.innerP[i]) % 1
                pos = min(int(round(1000 * progress)), 999)
                self.inner_planets[i].set_xdata([self.innerpos[i][0][pos]])
                self.inner_planets[i].set_ydata([self.innerpos[i][1][pos]])
                self.inner_planets[i].set_3d_properties([self.innerpos[i][2][pos]])
            self.innert += inc
            return (self.mercury, self.venus, self.earth, self.mars)

    def pause(self):
        self.active = 1-self.active
        self.pause_action.setIcon(self.stateicon[self.active])

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()






