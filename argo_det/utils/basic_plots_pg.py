import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore

def plot_variable_vs_depth_pg(data, variable):
    depth = data['depth']
    values = data[variable]

    # Create a PyQtGraph plot window
    app = QtWidgets.QApplication([])  # Initialize the app
    win = pg.GraphicsLayoutWidget(show=True, title=f"{variable.capitalize()} vs Depth")
    win.resize(800, 600)

    # Add a plot and configure the plot settings
    p = win.addPlot(title=f"{variable.capitalize()} vs Depth")
    p.invertY(True)  # Invert the y-axis to represent depth correctly
    p.setLabel('left', 'Depth', units='m')  # Set y-axis label
    p.setLabel('bottom', f"{variable.capitalize()} (units)")  # Set x-axis label
    p.showGrid(x=True, y=True)

    # Plot the data
    p.plot(values[0, :], depth[0, :], pen=pg.mkPen('w', width=2), name=variable)

    # Start the event loop
    QtWidgets.QApplication.instance().exec_()

def plot_variable_vs_time_pg(data, variable):
    time = data['time']
    values = data[variable]

    # Create a PyQtGraph plot window
    app = QtWidgets.QApplication([])  # Initialize the app
    win = pg.GraphicsLayoutWidget(show=True, title=f"{variable.capitalize()} vs Time")
    win.resize(800, 600)

    # Add a plot and configure the plot settings
    p = win.addPlot(title=f"{variable.capitalize()} vs Time")
    p.setLabel('left', f"{variable.capitalize()} (units)")  # Set y-axis label
    p.setLabel('bottom', 'Time (Julian Days)')  # Set x-axis label
    p.showGrid(x=True, y=True)

    # Plot the data
    p.plot(time, values[:, 0], pen=pg.mkPen('g', width=2), symbol='o', symbolBrush='b', name=variable)

    # Start the event loop
    QtWidgets.QApplication.instance().exec_()
