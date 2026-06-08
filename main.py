import sys
import ctypes

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from ui import DraftTrackerUI


if __name__ == "__main__":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "DirectStrikeTracker.App"
    )

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons/logo.ico"))

    window = DraftTrackerUI()
    window.setWindowIcon(QIcon("icons/logo.ico"))

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