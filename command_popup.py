from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt, Signal



class CommandPopup(QWidget):
    command_submitted = Signal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DST Command")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setFixedSize(300, 80)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Enter Command"))

        self.input = QLineEdit()
        self.input.returnPressed.connect(self.submit_command)

        layout.addWidget(self.input)
        self.setLayout(layout)

        self.hide()

    def show_popup(self):
        print("Showing popup")

        self.input.clear()
        self.show()
        self.showNormal()
        self.raise_()
        self.activateWindow()

        self.input.setFocus(Qt.ActiveWindowFocusReason)

    def submit_command(self):
        command = self.input.text().strip()

        if command:
            self.command_submitted.emit(command)

        self.hide()