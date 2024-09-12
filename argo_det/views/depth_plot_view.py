from PySide6.QtWidgets import QWidget, QHBoxLayout
import pyqtgraph as pg
import numpy as np

from argo_det.views.croppable_plot import CroppablePlotWidget
from argo_det.services.commands import CropCommand
from argo_det.services.command_manager import CommandManager, CentralCommandManager

# class DepthPlotView(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QHBoxLayout()

#         # Create 5 side-by-side pyqtgraph plots
#         self.plots = []
#         self.command_managers = []  # Command managers for each plot
#         self.command_manager = CentralCommandManager()

#         variables = ['Temperature', 'Salinity', 'Oxygen', 'Nitrate', 'pH']
#         for var in variables:
#             plot_widget = CroppablePlotWidget()
#             plot_widget.setLabel('bottom', var)
#             plot_widget.setLabel('left', 'Depth (m)')
#             plot_widget.getViewBox().invertY(True)  # Depth increases downwards
#             self.plots.append(plot_widget)
#             self.command_managers.append(CommandManager())
#             layout.addWidget(plot_widget)

#         self.setLayout(layout)

#         # Track data and profile index
#         self.data = None
#         self.profile_index = 0

#     def update_plots(self, data, profile_index=0):
#         """Updates the plots with data from a specific profile index."""
#         self.data = data  # Store data for further operations
#         self.profile_index = profile_index  # Store profile index for cropping

#         variables = ['temperature', 'salinity', 'oxygen', 'nitrate', 'ph']
#         for i, plot in enumerate(self.plots):
#             plot.clear()

#             # Extract the data for the specific profile
#             x_data = data[variables[i]][profile_index, :]  # Values (e.g., temperature, salinity)
#             y_data = data['depth'][profile_index, :]       # Depth values

#             # Remove invalid data points
#             valid_mask = ~np.isnan(x_data) & ~np.isnan(y_data)
            
#             # Plot the valid data
#             plot.set_line_data(x_data[valid_mask], y_data[valid_mask])  # Set line data in each plot widget
#             plot.getViewBox().autoRange()  # Automatically adjust the range of the plot

#     # def apply_crop(self):
#     #     """Applies the crop region to the plots by omitting the data within the region and updating the display."""
#     #     if self.data is None:
#     #         return  # If there's no data, nothing to crop

#     #     crop_regions = self.get_crop_regions()
#     #     variables = ['temperature', 'salinity', 'oxygen', 'nitrate', 'ph']

#     #     for i, plot in enumerate(self.plots):
#     #         region = crop_regions[i]
#     #         if region:
#     #             # Get the original data
#     #             x_data = self.data[variables[i]][self.profile_index, :]  # Values (e.g., temperature, salinity)
#     #             y_data = self.data['depth'][self.profile_index, :]       # Depth values

#     #             # Omit the data within the crop region
#     #             # We will split the line into segments: [before crop] and [after crop]
#     #             segment_masks = [(y_data < region[0]), (y_data > region[1])]

#     #             # Clear the current plot
#     #             plot.clear()

#     #             # Plot the segments (the line will break where the crop occurs)
#     #             for mask in segment_masks:
#     #                 cropped_x = x_data[mask]
#     #                 cropped_y = y_data[mask]

#     #                 # Plot each segment individually
#     #                 plot.plot(cropped_x, cropped_y, pen=pg.mkPen('w', width=2))

#     #             #plot.getViewBox().autoRange()  # Re-auto-range after crop

#     # def apply_crop(self):
#     #     """Applies the crop region to the plots and records it as a command."""
#     #     if self.data is None:
#     #         return  # If there's no data, nothing to crop

#     #     crop_regions = self.get_crop_regions()
#     #     variables = ['temperature', 'salinity', 'oxygen', 'nitrate', 'ph']

#     #     for i, plot in enumerate(self.plots):
#     #         region = crop_regions[i]
#     #         if region:
#     #             # Get the original data
#     #             x_data = self.data[variables[i]][self.profile_index, :]  # Values (e.g., temperature, salinity)
#     #             y_data = self.data['depth'][self.profile_index, :]       # Depth values

#     #             # Create a new crop command and execute it
#     #             crop_command = CropCommand(plot, x_data, y_data, region)
#     #             self.command_managers[i].execute_command(crop_command)

#     def apply_crop(self):
#         """Applies the crop region to the plots and records it as a command."""
#         if self.data is None:
#             return  # If there's no data, nothing to crop

#         crop_regions = self.get_crop_regions()
#         variables = ['temperature', 'salinity', 'oxygen', 'nitrate', 'ph']

#         for i, plot in enumerate(self.plots):
#             region = crop_regions[i]
#             if region:
#                 # Get the original data
#                 x_data = self.data[variables[i]][self.profile_index, :]  # Values (e.g., temperature, salinity)
#                 y_data = self.data['depth'][self.profile_index, :]       # Depth values

#                 # Create a new crop command and execute it
#                 crop_command = CropCommand(plot, x_data, y_data, region)
#                 self.command_manager.execute_command(crop_command)

#     def set_cropping(self, cropping: bool):
#         """Enable or disable cropping mode for all plot widgets."""
#         for plot in self.plots:
#             plot.set_cropping(cropping)

#     def get_crop_regions(self):
#         """Retrieve crop regions from all plot widgets."""
#         crop_regions = []
#         for plot in self.plots:
#             crop_region = plot.get_crop_region()
#             crop_regions.append(crop_region)
#         return crop_regions
    
#     # def undo(self):
#     #     """Undo the last crop on all plots."""
#     #     for manager in self.command_managers:
#     #         manager.undo()

#     # def redo(self):
#     #     """Redo the last undone crop on all plots."""
#     #     for manager in self.command_managers:
#     #         manager.redo()

#     def undo(self):
#         """Undo the last crop on the most recent plot."""
#         self.command_manager.undo()

#     def redo(self):
#         """Redo the last undone crop on the most recent plot."""
#         self.command_manager.redo()

class DepthPlotView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        # Create 5 side-by-side pyqtgraph plots
        self.plots = []
        self.command_manager = CentralCommandManager()  # Centralized command manager

        variables = [
            'Temperature', 
            'Salinity', 
            # 'Oxygen', 
            # 'Nitrate', 
            # 'pH'
        ]
        self.cumulative_masks = [None] * len(variables)  # Track cumulative masks for each plot

        for var in variables:
            plot_widget = CroppablePlotWidget()
            plot_widget.setLabel('bottom', var)
            plot_widget.setLabel('left', 'Depth (m)')
            plot_widget.getViewBox().invertY(True)  # Depth increases downwards
            self.plots.append(plot_widget)
            layout.addWidget(plot_widget)

        self.setLayout(layout)

        # Track data and profile index
        self.data = None
        self.profile_index = 0

    def update_plots(self, data, profile_index=0):
        """Updates the plots with data from a specific profile index."""
        self.data = data  # Store data for further operations
        self.profile_index = profile_index  # Store profile index for cropping

        variables = [
            'temperature', 
            'salinity', 
            # 'oxygen', 
            # 'nitrate', 
            # 'ph'
        ]
        for i, plot in enumerate(self.plots):
            plot.clear()

            # Extract the data for the specific profile
            x_data = data[variables[i]][profile_index, :]  # Values (e.g., temperature, salinity)
            y_data = data['depth'][profile_index, :]       # Depth values

            # Remove invalid data points
            valid_mask = ~np.isnan(x_data) & ~np.isnan(y_data)
            
            # Plot the valid data
            plot.set_line_data(x_data[valid_mask], y_data[valid_mask])  # Set line data in each plot widget
            plot.getViewBox().autoRange()  # Automatically adjust the range of the plot

            # Reset cumulative mask when a new plot is loaded
            self.cumulative_masks[i] = np.ones_like(y_data, dtype=bool)

    def apply_crop(self):
        """Applies the crop region to the plots and records it as a command."""
        if self.data is None:
            return  # If there's no data, nothing to crop

        crop_regions = self.get_crop_regions()
        variables = ['temperature', 'salinity', 'oxygen', 'nitrate', 'ph']

        for i, plot in enumerate(self.plots):
            region = crop_regions[i]
            if region:
                # Get the original data
                x_data = self.data[variables[i]][self.profile_index, :]  # Values (e.g., temperature, salinity)
                y_data = self.data['depth'][self.profile_index, :]       # Depth values

                # Create a new crop command and execute it
                crop_command = CropCommand(plot, x_data, y_data, region, self.cumulative_masks[i])
                self.command_manager.execute_command(crop_command)

                # Update the cumulative mask for this plot
                self.cumulative_masks[i] = crop_command.new_mask

    def set_cropping(self, cropping: bool):
        """Enable or disable cropping mode for all plot widgets."""
        for plot in self.plots:
            plot.set_cropping(cropping)

    def get_crop_regions(self):
        """Retrieve crop regions from all plot widgets."""
        crop_regions = []
        for plot in self.plots:
            crop_region = plot.get_crop_region()
            crop_regions.append(crop_region)
        return crop_regions

    def undo(self):
        """Undo the last crop on the most recent plot."""
        self.command_manager.undo()

    def redo(self):
        """Redo the last undone crop on the most recent plot."""
        self.command_manager.redo()

    def reset_command_manager(self):
        """Resets the command manager to clear all undo/redo history."""
        self.command_manager = CentralCommandManager()  # Reset the command manager

    def switch_profile(self, new_profile):
        """Switch to a new profile and reset the command manager."""
        self.reset_command_manager()  # Reset command manager on profile switch
        self.profile_index = new_profile
        self.update_plots(self.data, new_profile)

    def switch_file(self, new_file_data):
        """Switch to a new file and reset the command manager."""
        self.reset_command_manager()  # Reset command manager on file switch
        self.data = new_file_data
        self.update_plots(new_file_data)


    def switch_mode(self, mode: str):
        for plot in self.plots:
            plot.mode = mode