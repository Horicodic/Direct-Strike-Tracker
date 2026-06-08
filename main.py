import sys
import os
import ctypes
import keyboard

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QObject, Signal

from ui import DraftTrackerUI
from command_popup import CommandPopup
from command_parser import parse_command


class HotkeyBridge(QObject):
    show_popup = Signal()


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

    popup = CommandPopup()
    popup.setWindowIcon(icon)

    bridge = HotkeyBridge()
    bridge.show_popup.connect(popup.show_popup)

    def handle_command(command):
        result = parse_command(command)

        print("Command:", command)
        print("Parsed:", result)

        if not result:
            return

        enemy_index = result["enemy"] - 1
        unit_name = result["unit"]

        window.enemy_panels[enemy_index].select_unit_by_name(unit_name)

    popup.command_submitted.connect(handle_command)

    keyboard.add_hotkey(
        "alt+d",
        bridge.show_popup.emit
    )

    window.show()

    exit_code = app.exec()

    keyboard.unhook_all_hotkeys()

    sys.exit(exit_code)