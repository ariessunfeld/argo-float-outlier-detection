
"""This module contains a subclass of pyqtgraph.PlotWidget that allows for cropping"""

from PySide6 import QtCore
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
import pyqtgraph as pg
import numpy as np

class CroppablePlotWidget(pg.PlotWidget):

    point_added = Signal(float, float)  # emits x, y of new point
    point_removed = Signal(int)  # emits idx of removed point

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cropping = False
        self.start_crop_pos = None
        self.crop_region = None
        self.points = {'x': np.array([]), 'y': np.array([])}
        self.mode = 'normal'

        # Set up mouse click event for adding points in empty space
        self.scene().sigMouseClicked.connect(self.on_scene_click)
        
        self.setFocusPolicy(Qt.StrongFocus)

    def get_crop_region(self):
        """Retrieve the current crop region (start and end y values) if it exists."""
        if self.crop_region is not None:
            region = self.crop_region.getRegion()  # Get the start and end y-values
            return region
        return None
    
    def set_crop_region(self, start_y: float, end_y: float):
        """Set the crop region (vertical selection) based on start and end y values."""
        self.start_crop_pos = start_y

        if self.crop_region is None:
            # Vertical cropping region (based on y-axis)
            self.crop_region = pg.LinearRegionItem([self.start_crop_pos, end_y], 
                                                orientation=pg.LinearRegionItem.Horizontal, 
                                                movable=False, 
                                                brush=pg.mkBrush(128, 128, 128, 100))
            self.addItem(self.crop_region)
        else:
            self.crop_region.setRegion([self.start_crop_pos, end_y])

    def mousePressEvent(self, event):
        if self.cropping:
            self.start_crop_pos = self.getPlotItem().vb.mapSceneToView(QtCore.QPointF(event.pos())).y()  # Capture y-coordinate
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.cropping:
            self.start_crop_pos = None  # Reset start position
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        if self.cropping:
            if event.buttons() == Qt.LeftButton:  # Check if left mouse button is pressed
                if self.start_crop_pos is not None:
                    end_crop_pos = self.getPlotItem().vb.mapSceneToView(QtCore.QPointF(pos)).y()  # Use y-coordinate for vertical selection
                    self.set_crop_region(self.start_crop_pos, end_crop_pos)
                event.accept()
            else:
                event.ignore()
        else:
            super().mouseMoveEvent(event)

    def on_scene_click(self, event):
        if not self.cropping:  # Only handle click if cropping is not active
            if event.button() == Qt.LeftButton:
                pos = event.scenePos()
                mousePoint = self.plotItem.vb.mapSceneToView(pos)
                x_click, y_click = mousePoint.x(), mousePoint.y()

                x, y = self.points['x'], self.points['y']
                if len(x) and len(y):
                    distances = np.hypot(x - x_click, y - y_click)
                    closest_point_idx = np.argmin(distances)
                    threshold = 0.1  # Threshold for detecting clicks on points

                    # Check if the click is on an existing point
                    click_on_point = distances[closest_point_idx] < threshold
                else:
                    click_on_point = False

                if self.mode == 'add' and not click_on_point:
                    print("Adding a new point")
                    self.points['x'] = np.append(self.points['x'], x_click)
                    self.points['y'] = np.append(self.points['y'], y_click)
                    self.point_added.emit(x_click, y_click)
                    self.update_plot()

    def on_point_click(self, plot, points):
        if not self.cropping:  # Only handle point clicks if cropping is not active
            print(f'Inside on_point_clicked, {points=}')
            pos = points[0].pos()
            x_click, y_click = pos.x(), pos.y()
            print(f"Point clicked at: x={x_click}, y={y_click}")
            print(f'{self.mode=}')

            x, y = self.points['x'], self.points['y']
            distances = np.hypot(x - x_click, y - y_click)
            closest_point_idx = np.argmin(distances)
            threshold = 0.1  # Threshold for detecting clicks on points

            if self.mode == 'delete' and distances[closest_point_idx] < threshold:
                print(f"Removing point: {closest_point_idx}")
                self.points['x'] = np.delete(self.points['x'], closest_point_idx)
                self.points['y'] = np.delete(self.points['y'], closest_point_idx)
                self.point_removed.emit(closest_point_idx)
                #self.update_plot()
                self.update_line_plot()

    def set_line_data(self, x, y):
        """Set the raw data for the line plot."""
        self.points['x'] = np.array(x)
        self.points['y'] = np.array(y)
        self.update_line_plot()  # Automatically replot with the new data
        #self.update_plot()

    def update_line_plot(self, crop_region=None):
        """Update the plot, applying the crop region if provided, for a line plot."""
        # If there's a line plot already, remove it
        if hasattr(self, 'line'):
            self.removeItem(self.line)

        x_data, y_data = self.points['x'], self.points['y']

        # Apply crop if there's a crop region
        if crop_region:
            valid_mask = (y_data >= crop_region[0]) & (y_data <= crop_region[1])
            x_data, y_data = x_data[valid_mask], y_data[valid_mask]

        # Plot a line with the (potentially cropped) data
        self.line = pg.PlotDataItem(x_data, y_data, pen=pg.mkPen('w', width=2), symbol='o', symbolSize=5, symbolBrush=(255, 255, 255))  # Change 'r' for a color you like
        self.line.sigPointsClicked.connect(self.on_point_click)
        self.addItem(self.line)

    def update_plot(self):
        if hasattr(self, 'scatter'):
            self.removeItem(self.scatter)
        self.scatter = pg.ScatterPlotItem(self.points['x'], self.points['y'], pen='r', symbol='o', symbolSize=7, symbolBrush=(255, 0, 0))
        self.scatter.sigClicked.connect(self.on_point_click)  # Reconnect the signal to handle point clicks
        self.addItem(self.scatter)

    def set_scatter(self, x, y):
        self.points['x'] = np.array(x)
        self.points['y'] = np.array(y)
        self.update_plot()

    def set_cropping(self, cropping: bool):
        """Enables or disables cropping mode."""
        self.cropping = cropping
        if not cropping:
            self.clear_crop_region()

    def clear_crop_region(self):
        """Removes the crop region from the plot."""
        if self.crop_region is not None:
            self.removeItem(self.crop_region)
            self.crop_region = None
