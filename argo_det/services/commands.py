import numpy as np
import pyqtgraph as pg

class Command:
    """Base class for all commands."""
    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

# class CropCommand(Command):
#     """Command to crop a plot by omitting a region."""
#     def __init__(self, plot, x_data, y_data, crop_region):
#         self.plot = plot
#         self.x_data = x_data.copy()  # Original data
#         self.y_data = y_data.copy()  # Original data
#         self.crop_region = crop_region
#         self.previous_mask = None    # To store previous valid mask for undo

#     def execute(self):
#         """Apply the crop by omitting the data within the crop region."""
#         # Store the previous valid mask if available (for undo purposes)
#         if self.previous_mask is None:
#             self.previous_mask = np.ones_like(self.y_data, dtype=bool)

#         # Calculate the new valid mask
#         new_mask = (self.y_data < self.crop_region[0]) | (self.y_data > self.crop_region[1])

#         # Combine the new mask with the previous mask (cumulative cropping)
#         combined_mask = self.previous_mask & new_mask

#         # Update the plot with the combined mask
#         cropped_x = np.where(combined_mask, self.x_data, np.nan)
#         cropped_y = np.where(combined_mask, self.y_data, np.nan)
        
#         self.plot.clear()
#         self.plot.plot(cropped_x, cropped_y, pen=pg.mkPen('w', width=2))

#         # Update the previous mask for future crops
#         self.previous_mask = combined_mask

#     def undo(self):
#         """Undo the crop by restoring the original data."""
#         self.plot.clear()
#         self.plot.plot(self.x_data, self.y_data, pen=pg.mkPen('w', width=2))

#         # Reset the mask so future crops act on the original data
#         self.previous_mask = np.ones_like(self.y_data, dtype=bool)

# class CropCommand(Command):
#     """Command to crop a plot by omitting a region."""
#     def __init__(self, plot, x_data, y_data, crop_region):
#         self.plot = plot
#         self.x_data = x_data.copy()  # Original data
#         self.y_data = y_data.copy()  # Original data
#         self.crop_region = crop_region
#         self.previous_mask = None    # To store previous valid mask for undo

#     def execute(self):
#         """Apply the crop by omitting the data within the crop region."""
#         if self.previous_mask is None:
#             self.previous_mask = np.ones_like(self.y_data, dtype=bool)

#         print('Executing a crop')
#         print('self.previous_mask:', self.previous_mask)

#         new_mask = (self.y_data < self.crop_region[0]) | (self.y_data > self.crop_region[1])

#         print('new_mask:', new_mask)

#         # Combine the new mask with the previous one for cumulative cropping
#         combined_mask = self.previous_mask & new_mask

#         print('combined_mask:', combined_mask)

#         cropped_x = np.where(combined_mask, self.x_data, np.nan)
#         cropped_y = np.where(combined_mask, self.y_data, np.nan)

#         self.plot.clear()
#         self.plot.plot(cropped_x, cropped_y, pen=pg.mkPen('w', width=2))

#         self.previous_mask = combined_mask

#     def undo(self):
#         """Undo the crop by restoring the original data."""
#         self.plot.clear()
#         self.plot.plot(self.x_data, self.y_data, pen=pg.mkPen('w', width=2))

#         # Reset the mask to the full range for further actions
#         self.previous_mask = np.ones_like(self.y_data, dtype=bool)

class CropCommand(Command):
    """Command to crop a plot by omitting a region."""
    def __init__(self, plot, x_data, y_data, crop_region, previous_mask):
        self.plot = plot
        self.x_data = x_data.copy()  # Original data
        self.y_data = y_data.copy()  # Original data
        self.crop_region = crop_region
        self.previous_mask = previous_mask.copy() if previous_mask is not None else np.ones_like(self.y_data, dtype=bool)
        self.new_mask = None  # To store the newly combined mask after applying the crop

    def execute(self):
        """Apply the crop cumulatively, updating the mask."""
        # Create a new mask for this crop
        crop_mask = (self.y_data < self.crop_region[0]) | (self.y_data > self.crop_region[1])

        # Combine the previous mask with the new crop mask (cumulative cropping)
        self.new_mask = self.previous_mask & crop_mask

        # Apply the new cumulative mask
        cropped_x = np.where(self.new_mask, self.x_data, np.nan)
        cropped_y = np.where(self.new_mask, self.y_data, np.nan)

        self.plot.clear()
        self.plot.plot(cropped_x, cropped_y, pen=pg.mkPen('w', width=2), symbol='o', symbolSize=5, symbolBrush=(255, 255, 255))

    def undo(self):
        """Undo the crop by restoring the previous mask."""
        # Use the previous mask to undo the last crop
        cropped_x = np.where(self.previous_mask, self.x_data, np.nan)
        cropped_y = np.where(self.previous_mask, self.y_data, np.nan)

        self.plot.clear()
        self.plot.plot(cropped_x, cropped_y, pen=pg.mkPen('w', width=2), symbol='o', symbolSize=5, symbolBrush=(255, 255, 255))

