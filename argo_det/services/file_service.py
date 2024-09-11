
from argo_det.utils.ingestion import load_argo_data

class FileService:
    def __init__(self, file_model):
        self.file_model = file_model

    def load_file_data(self, file_name):
        """Load and return the data from the selected .nc file."""
        file_path = self.file_model.set_current_file(file_name)
        return load_argo_data(file_path)
