import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from itertools import product, combinations

class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.hemisphere_center = [0, 0, 0]  # Center of the hemisphere
        self.box_size = 1  # Size of the box
        self.hemisphere_radius = self.box_size / 5  # Radius of the hemisphere
        self.initUI()

    def initUI(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Vertical layout
        layout = QVBoxLayout(self.main_widget)

        # Matplotlib Figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Theta Slider
        self.theta_slider = QSlider(Qt.Horizontal)
        self.theta_slider.setRange(0, 314)  # 0 to pi, scaled by 100
        self.theta_slider.setValue(157)  # pi/2
        self.theta_slider.valueChanged[int].connect(self.update_plot)
        layout.addWidget(self.theta_slider)

        # Phi Slider
        self.phi_slider = QSlider(Qt.Horizontal)
        self.phi_slider.setRange(0, 628)  # 0 to 2*pi, scaled by 100
        self.phi_slider.setValue(314)  # pi
        self.phi_slider.valueChanged[int].connect(self.update_plot)
        layout.addWidget(self.phi_slider)

        # Initial plot setup
        self.setup_initial_plot()

    def setup_initial_plot(self):
        self.ax = self.figure.add_subplot(111, projection='3d')
        plot_box(self.ax, self.box_size)
        plot_hemisphere(self.ax, self.hemisphere_radius, self.hemisphere_center)
        self.line, = self.ax.plot([], [], [], color='red')
        self.set_plot_limits_and_labels()

    def set_plot_limits_and_labels(self):
        self.ax.set_xlim([-self.box_size/2, self.box_size/2])
        self.ax.set_ylim([-self.box_size/2, self.box_size/2])
        self.ax.set_zlim([-self.box_size/2, self.box_size/2])
        self.ax.set_xlabel('X Axis')
        self.ax.set_ylabel('Y Axis')
        self.ax.set_zlabel('Z Axis')

    def update_plot(self):
        theta = self.theta_slider.value() / 100.0
        phi = self.phi_slider.value() / 100.0

        # Calculate end point of the line
        x = self.hemisphere_radius * np.sin(theta) * np.cos(phi)
        y = self.hemisphere_radius * np.sin(theta) * np.sin(phi)
        z = self.hemisphere_radius * np.cos(theta)
        end_point = [self.hemisphere_center[0] + x, self.hemisphere_center[1] + y, self.hemisphere_center[2] + z]

        # Update line data
        self.line.set_data_3d([self.hemisphere_center[0], end_point[0]], 
                              [self.hemisphere_center[1], end_point[1]], 
                              [self.hemisphere_center[2], end_point[2]])

        # Update the canvas
        self.canvas.draw_idle()

# Function to plot the box
def plot_box(ax, size):
    r = [-size/2, size/2]
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            ax.plot3D(*zip(s, e), color="black", alpha=0.3)

# Function to plot the hemisphere
def plot_hemisphere(ax, radius, center):
    phi, theta = np.mgrid[0:np.pi:100j, 0:2*np.pi:100j]
    x = center[0] + radius * np.sin(phi) * np.cos(theta)
    y = center[1] + radius * np.sin(phi) * np.sin(theta)
    z = center[2] + radius * np.cos(phi)
    z[z < center[2]] = np.nan
    ax.plot_surface(x, y, z, color='b', alpha=0.3)

def main():
    app = QApplication(sys.argv)
    mainWin = PlotWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

