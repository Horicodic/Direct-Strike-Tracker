import sys
import os
import ctypes

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from ui import DraftTrackerUI


def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "Horia.DirectStrikeTracker.App"
    )

    app = QApplication(sys.argv)

    icon = QIcon(resource_path("icons/logo.ico"))
    app.setWindowIcon(icon)

    window = DraftTrackerUI()
    window.setWindowIcon(icon)

    window.setWindowFlags(
        Qt.Window |
        Qt.WindowTitleHint |
        Qt.WindowSystemMenuHint |
        Qt.WindowMinimizeButtonHint |
        Qt.WindowMaximizeButtonHint |
        Qt.WindowCloseButtonHint
    )

    window.show()

    sys.exit(app.exec())