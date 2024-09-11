from PySide6.QtWidgets import QWidget, QHBoxLayout
import pyqtgraph as pg
import numpy as np

class DepthPlotView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        # Create 5 side-by-side pyqtgraph plots
        self.plots = []
        variables = ['Temperature', 'Salinity', 'Oxygen', 'Nitrate', 'pH']
        for var in variables:
            plot_widget = pg.PlotWidget()
            plot_widget.setLabel('bottom', var)
            plot_widget.setLabel('left', 'Depth (m)')
            plot_widget.getViewBox().invertY(True)  # Depth increases downwards
            self.plots.append(plot_widget)
            layout.addWidget(plot_widget)

        self.setLayout(layout)

    def update_plots(self, data, profile_index=0):
        """Updates the plots with data from a specific profile index."""
        variables = ['temperature', 'salinity', 'oxygen', 'nitrate', 'ph']
        for i, plot in enumerate(self.plots):
            plot.clear()

            # Extract the data for the specific profile, same as the working matplotlib logic
            x_data = data[variables[i]][profile_index, :]  # Values (e.g., temperature, salinity)
            y_data = data['depth'][profile_index, :]       # Depth values

            # Remove invalid data points
            valid_mask = ~np.isnan(x_data) & ~np.isnan(y_data)
            
            # Plot the valid data
            plot.plot(x_data[valid_mask], y_data[valid_mask], pen=pg.mkPen('w', width=2))
            plot.getViewBox().autoRange()  # Automatically adjust the range of the plot
