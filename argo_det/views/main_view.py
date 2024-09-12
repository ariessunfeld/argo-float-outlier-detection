# from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QStackedWidget

# class MainView(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Argo Float Outlier Detection")
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)

#         # Top bar elements (folder selection, dropdown, etc.)
#         top_bar = QHBoxLayout()

#         self.select_folder_btn = QPushButton("Select Folder")
#         self.selected_folder_label = QLabel("No folder selected")
#         self.file_dropdown = QComboBox()
#         self.next_file_btn = QPushButton("Next File")

#         top_bar.addWidget(self.select_folder_btn)
#         top_bar.addWidget(self.selected_folder_label)
#         top_bar.addWidget(self.file_dropdown)
#         top_bar.addWidget(self.next_file_btn)

#         self.layout.addLayout(top_bar)

#         # Create a stacked widget for switching between the views (Depth and Time plots)
#         self.stack = QStackedWidget()
#         self.layout.addWidget(self.stack)

#     def add_depth_plot_view(self, depth_view):
#         """Add the depth plot view to the stack."""
#         self.stack.addWidget(depth_view)

#     def add_time_plot_view(self, time_view):
#         """Add the time plot view to the stack."""
#         self.stack.addWidget(time_view)

#     def show_depth_plot(self):
#         """Show the depth plot view."""
#         self.stack.setCurrentIndex(0)

#     def show_time_plot(self):
#         """Show the time plot view."""
#         self.stack.setCurrentIndex(1)


from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QStackedWidget

class MainView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Argo Float Outlier Detection")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Top bar elements (folder selection, file dropdown, next button)
        top_bar = QHBoxLayout()

        self.select_folder_btn = QPushButton("Select Folder")
        self.selected_folder_label = QLabel("No folder selected")
        self.file_dropdown = QComboBox()
        self.profile_dropdown = QComboBox()  # Profile selector dropdown
        self.next_file_btn = QPushButton("Next File")
        self.next_profile_btn = QPushButton("Next Profile")
        self.crop_mode_btn = QPushButton("Enter Crop Mode")
        self.mode_selection = QComboBox()
        self.mode_selection.addItems(['Normal', 'Delete'])
        self.undo_btn = QPushButton("Undo")
        self.redo_btn = QPushButton("Redo")

        top_bar.addWidget(self.select_folder_btn)
        top_bar.addWidget(self.selected_folder_label)
        top_bar.addWidget(self.file_dropdown)
        top_bar.addWidget(self.profile_dropdown)  # Add profile selector to top bar
        top_bar.addWidget(self.next_file_btn)
        top_bar.addWidget(self.next_profile_btn)
        top_bar.addWidget(self.crop_mode_btn)
        top_bar.addWidget(self.mode_selection)
        # top_bar.addWidget(self.undo_btn)
        # top_bar.addWidget(self.redo_btn)

        self.layout.addLayout(top_bar)

        # Create a stacked widget for switching between the views (Depth and Time plots)
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

    def add_depth_plot_view(self, depth_view):
        """Add the depth plot view to the stack."""
        self.stack.addWidget(depth_view)

    def add_time_plot_view(self, time_view):
        """Add the time plot view to the stack."""
        self.stack.addWidget(time_view)

    def show_depth_plot(self):
        """Show the depth plot view."""
        self.stack.setCurrentIndex(0)

    def show_time_plot(self):
        """Show the time plot view."""
        self.stack.setCurrentIndex(1)

    def set_profile_list(self, profile_numbers):
        """Populate the profile selector dropdown with profile numbers."""
        self.profile_dropdown.clear()
        self.profile_dropdown.addItems([str(num) for num in profile_numbers])
        self.profile_dropdown.setCurrentIndex(0)  # Default to first profile
