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

        # Initial plot
        self.update_plot()

    def update_plot(self):
        theta = self.theta_slider.value() / 100.0
        phi = self.phi_slider.value() / 100.0

        ax = self.figure.add_subplot(111, projection='3d', label="Base")
        ax.clear()

        # Parameters
        box_size = 1
        hemisphere_radius = box_size / 8
        hemisphere_center = [0,0,0]
        laser_length = box_size
        start_point = hemisphere_center
        direction = np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])
        end_point = start_point + direction * laser_length

        # Plot box
        r = [-box_size/2, box_size/2]
        for s, e in combinations(np.array(list(product(r, r, r))), 2):
            if np.sum(np.abs(s-e)) == r[1]-r[0]:
                ax.plot3D(*zip(s, e), color="black", alpha=0.3)

        # Plot hemisphere
        phi, theta = np.mgrid[0:np.pi:100j, 0:2*np.pi:100j]
        x = hemisphere_center[0] + hemisphere_radius * np.sin(phi) * np.cos(theta)
        y = hemisphere_center[1] + hemisphere_radius * np.sin(phi) * np.sin(theta)
        z = hemisphere_center[2] + hemisphere_radius * np.cos(phi)
        z[z < hemisphere_center[2]] = np.nan
        ax.plot_surface(x, y, z, color='b', alpha=0.3)

               # Plot line
        ax.plot([start_point[0], end_point[0]], 
                [start_point[1], end_point[1]], 
                [start_point[2], end_point[2]], color='red')

        # Set plot limits and labels
        ax.set_xlim([-box_size/2, box_size/2])
        ax.set_ylim([-box_size/2, box_size/2])
        ax.set_zlim([-box_size/2, box_size/2])
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_zlabel('Z Axis')

        # Update the canvas
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    mainWin = PlotWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

