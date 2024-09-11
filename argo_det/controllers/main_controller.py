
from PySide6.QtWidgets import QFileDialog

# class MainController:
#     def __init__(self, main_view, file_model, file_service, depth_view, time_view):
#         self.main_view = main_view
#         self.file_model = file_model
#         self.file_service = file_service
#         self.depth_view = depth_view
#         self.time_view = time_view

#         self.current_profile_index = 0  # Initialize the profile index

#         # Add the views to the main view
#         self.main_view.add_depth_plot_view(self.depth_view)
#         self.main_view.add_time_plot_view(self.time_view)

#         # Set up connections
#         self.setup_connections()

#     def setup_connections(self):
#         """Connects the view elements to controller methods."""
#         self.main_view.select_folder_btn.clicked.connect(self.select_folder)
#         self.main_view.file_dropdown.currentTextChanged.connect(self.update_plots)
#         self.main_view.next_file_btn.clicked.connect(self.next_file)

#     def select_folder(self):
#         """Handles folder selection and updates the view."""
#         folder_path = QFileDialog.getExistingDirectory(self.main_view, "Select Folder")
#         if folder_path:
#             files = self.file_model.load_folder(folder_path)
#             self.main_view.selected_folder_label.setText(folder_path)
#             self.main_view.file_dropdown.clear()
#             self.main_view.file_dropdown.addItems(files)

#     def update_plots(self, file_name):
#         """Updates the depth or time plots based on the selected file."""
#         if file_name:
#             data = self.file_service.load_file_data(file_name)
#             self.depth_view.update_plots(data, profile_index=self.current_profile_index)
#             self.main_view.show_depth_plot()  # Switch to the depth plot view

#     def next_file(self):
#         """Moves to the next file in the folder."""
#         current_index = self.main_view.file_dropdown.currentIndex()
#         next_index = (current_index + 1) % self.main_view.file_dropdown.count()
#         self.main_view.file_dropdown.setCurrentIndex(next_index)

class MainController:
    def __init__(self, main_view, file_model, file_service, depth_view, time_view):
        self.main_view = main_view
        self.file_model = file_model
        self.file_service = file_service
        self.depth_view = depth_view
        self.time_view = time_view

        self.current_profile_index = 0  # Initialize the profile index

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
        self.main_view.next_file_btn.clicked.connect(self.next_file)
        self.main_view.next_profile_btn.clicked.connect(self.next_profile)

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
