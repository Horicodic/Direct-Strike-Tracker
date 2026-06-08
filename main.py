import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui import DraftTrackerUI


class App(DraftTrackerUI):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.Tool
        )

       


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())