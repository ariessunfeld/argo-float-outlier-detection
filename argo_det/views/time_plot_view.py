
from PySide6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg

class TimePlotView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Create a time plot for selected variable
        self.time_plot = pg.PlotWidget()
        self.time_plot.setLabel('bottom', 'Time')
        self.time_plot.setLabel('left', 'Variable')
        layout.addWidget(self.time_plot)

        self.setLayout(layout)

    def update_plot(self, data, variable):
        """Updates the time plot with new data."""
        self.time_plot.clear()
        self.time_plot.plot(data['time'], data[variable])
