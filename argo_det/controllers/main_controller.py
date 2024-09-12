
from PySide6.QtWidgets import QFileDialog

class MainController:
    def __init__(self, main_view, file_model, file_service, depth_view, time_view):
        self.main_view = main_view
        self.file_model = file_model
        self.file_service = file_service
        self.depth_view = depth_view
        self.time_view = time_view
        self.current_profile_index = 0 
        self.is_cropping = False

        # Add the views to the main view
        self.main_view.add_depth_plot_view(self.depth_view)
        self.main_view.add_time_plot_view(self.time_view)

        # Set up connections
        self.setup_connections()

    def setup_connections(self):
        """Connects the view elements to controller methods."""
        self.main_view.select_folder_btn.clicked.connect(self.select_folder)
        self.main_view.file_dropdown.currentTextChanged.connect(self.update_plots)
        self.main_view.profile_dropdown.currentTextChanged.connect(self.update_profile)
        self.main_view.mode_selection.currentTextChanged.connect(self.update_mode)
        self.main_view.next_file_btn.clicked.connect(self.next_file)
        self.main_view.next_profile_btn.clicked.connect(self.next_profile)
        self.main_view.crop_mode_btn.clicked.connect(self.toggle_crop_mode)
        self.main_view.undo_btn.clicked.connect(self.undo_crop)
        self.main_view.redo_btn.clicked.connect(self.redo_crop)


    def select_folder(self):
        """Handles folder selection and updates the view."""
        folder_path = QFileDialog.getExistingDirectory(self.main_view, "Select Folder")
        if folder_path:
            files = self.file_model.load_folder(folder_path)
            self.main_view.selected_folder_label.setText(folder_path)
            self.main_view.file_dropdown.clear()
            self.main_view.file_dropdown.addItems(files)

    def update_plots(self, file_name):
        """Updates the depth or time plots based on the selected file."""
        if file_name:
            data = self.file_service.load_file_data(file_name)
            self.current_profile_index = 0  # Reset profile index when new file is selected
            num_profiles = data['depth'].shape[0]  # Get number of profiles from the data
            self.main_view.set_profile_list(range(num_profiles))  # Populate profile selector

            self.depth_view.update_plots(data, profile_index=self.current_profile_index)
            self.main_view.show_depth_plot()  # Switch to the depth plot view

    def update_profile(self, profile_number):
        """Handles profile selection and updates the plots."""
        if profile_number.isdigit():  # Only update if profile_number is a valid digit
            self.current_profile_index = int(profile_number)  # Update the current profile index
            file_name = self.main_view.file_dropdown.currentText()  # Get the selected file
            if file_name:
                data = self.file_service.load_file_data(file_name)
                self.depth_view.update_plots(data, profile_index=self.current_profile_index)

    def next_file(self):
        """Moves to the next file in the folder."""
        current_index = self.main_view.file_dropdown.currentIndex()
        next_index = (current_index + 1) % self.main_view.file_dropdown.count()
        self.main_view.file_dropdown.setCurrentIndex(next_index)

    def next_profile(self):
        """Moves to the next profile in the dropdown."""
        current_index = self.main_view.profile_dropdown.currentIndex()
        next_index = (current_index + 1) % self.main_view.profile_dropdown.count()
        self.main_view.profile_dropdown.setCurrentIndex(next_index)

    def toggle_crop_mode(self):
        """Toggles between crop mode and apply crop."""
        if not self.is_cropping:
            self.is_cropping = True
            self.depth_view.set_cropping(True)  # Enable cropping in all plot widgets
            self.main_view.crop_mode_btn.setText("Apply Crop")
        else:
            self.is_cropping = False
            self.apply_crop()
            self.depth_view.set_cropping(False)  # Disable cropping in all plot widgets
            self.main_view.crop_mode_btn.setText("Enter Crop Mode")

    def apply_crop(self):
        """Applies the crop regions to the current plots."""
        self.depth_view.apply_crop()
        crop_regions = self.depth_view.get_crop_regions()
        for i, region in enumerate(crop_regions):
            if region:
                print(f"Applying crop on plot {i} (0-indexed): from {region[0]} to {region[1]}")
                # Can add code here to handle the cropped data

    def update_mode(self):
        curr_mode = self.main_view.mode_selection.currentText().lower()
        self.depth_view.switch_mode(curr_mode)

    def undo_crop(self):
        """Undo the last crop."""
        self.depth_view.undo()

    def redo_crop(self):
        """Redo the last undone crop."""
        self.depth_view.redo()
