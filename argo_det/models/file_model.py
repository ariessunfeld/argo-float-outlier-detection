
import os

class FileModel:
    def __init__(self):
        self.folder_path = None
        self.files = []
        self.current_file = None

    def load_folder(self, folder_path):
        """Load .nc files from the selected folder."""
        self.folder_path = folder_path
        self.files = [f for f in os.listdir(folder_path) if f.endswith('.nc')]
        return self.files

    def set_current_file(self, file_name):
        """Set the current file and return the full file path."""
        self.current_file = os.path.join(self.folder_path, file_name)
        return self.current_file
