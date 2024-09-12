
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import qInstallMessageHandler

from argo_det.controllers.main_controller import MainController
from argo_det.models.file_model import FileModel
from argo_det.services.file_service import FileService
from argo_det.views.main_view import MainView
from argo_det.views.depth_plot_view import DepthPlotView
from argo_det.views.time_plot_view import TimePlotView


def suppress_qt_messages(*args):
    pass


def main():

    os.environ["QT_LOGGING_RULES"] = "qt.pointer.dispatch.debug=false"
    qInstallMessageHandler(suppress_qt_messages)

    app = QApplication([])

    # Instantiate models, views, and services
    file_model = FileModel()
    file_service = FileService(file_model)
    main_view = MainView()
    depth_view = DepthPlotView()
    time_view = TimePlotView()

    # Instantiate the main controller and connect everything
    controller = MainController(main_view, file_model, file_service, depth_view, time_view)

    # Show the main view
    main_view.show()

    app.exec()

if __name__ == "__main__":
    main()
