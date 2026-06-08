import os

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLabel,
    QScrollArea, QSizePolicy,
    QPushButton, QGridLayout
)

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt

from units import UNITS_BY_HOTKEY


# -------------------------
# path helper
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def asset_path(path):
    return os.path.join(BASE_DIR, path)


# -------------------------
# clickable top draft icon
# -------------------------
class DraftIcon(QLabel):
    def __init__(self, hotkey, unit_name, icon_path, on_remove_callback):
        super().__init__()

        self.hotkey = hotkey
        self.unit_name = unit_name
        self.on_remove_callback = on_remove_callback

        pixmap = QPixmap(asset_path(icon_path))
        self.setPixmap(pixmap.scaled(48, 48, Qt.KeepAspectRatio))

        self.setToolTip(unit_name)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.on_remove_callback(self.hotkey, self.unit_name)


# -------------------------
# unit button
# -------------------------
class UnitPortrait(QPushButton):
    def __init__(self, name, icon_path):
        super().__init__()

        self.unit_name = name
        self.icon_path = icon_path
        self.hotkey = None

        self.setCheckable(True)
        self.setFixedSize(64, 64)

        pixmap = QPixmap(asset_path(icon_path))
        if pixmap.isNull():
            print(f"[ERROR] Missing image: {icon_path}")

        self.setIcon(QIcon(pixmap))
        self.setIconSize(QSize(56, 56))
        self.setToolTip(name)

        self.toggled.connect(self.update_style)
        self.update_style()

    def update_style(self):
        if self.isChecked():
            self.setStyleSheet("""
                QPushButton {
                    border: 2px solid lime;
                    background-color: rgba(0,255,0,40);
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    border: 1px solid gray;
                    background-color: transparent;
                }
            """)


# -------------------------
# enemy panel
# -------------------------
class EnemyPanel(QGroupBox):
    def __init__(self, name):
        super().__init__(name)

        layout = QVBoxLayout()

        # -------------------------
        # controls
        # -------------------------
        controls = QHBoxLayout()

        collapse_all_btn = QPushButton("Collapse All")
        expand_all_btn = QPushButton("Expand All")

        collapse_all_btn.setFixedHeight(24)
        expand_all_btn.setFixedHeight(24)

        collapse_all_btn.clicked.connect(self.collapse_all_categories)
        expand_all_btn.clicked.connect(self.expand_all_categories)

        controls.addWidget(collapse_all_btn)
        controls.addWidget(expand_all_btn)

        layout.addLayout(controls)

        # -------------------------
        # top draft bar
        # -------------------------
        self.draft_grid = QGridLayout()
        self.slot_map = {}
        self.group_selected = {}

        draft_container = QWidget()
        draft_container.setLayout(self.draft_grid)
        draft_container.setFixedHeight(180)

        layout.addWidget(draft_container)

        # -------------------------
        # state
        # -------------------------
        self.group_buttons = {}
        self.category_content = {}
        self.category_headers = {}

        self.hotkey_position = {
            "Q": (0, 0),
            "W": (0, 1),
            "E": (0, 2),
            "R": (0, 3),

            "A": (1, 0),
            "S": (1, 1),
            "D": (1, 2),
            "F": (1, 3),

            "Z": (2, 0),
            "X": (2, 1),
            "C": (2, 2),
        }

        # -------------------------
        # categories
        # -------------------------
        for hotkey, units in UNITS_BY_HOTKEY.items():

            container = QWidget()
            vbox = QVBoxLayout(container)

            header = QLabel(f" {hotkey} ")
            header.setAlignment(Qt.AlignCenter)
            header.setFixedHeight(24)

            header.setStyleSheet(f"""
                QLabel {{
                    font-weight: bold;
                    color: white;
                    background-color: {self.get_hotkey_color(hotkey)};
                    border: 2px solid #333;
                    border-radius: 6px;
                }}
                QLabel:hover {{
                    border: 2px solid white;
                }}
            """)

            vbox.addWidget(header)

            content = QWidget()
            grid = QGridLayout(content)

            self.group_buttons[hotkey] = []
            self.category_content[hotkey] = content
            self.category_headers[hotkey] = header

            for i, (unit_name, icon_path) in enumerate(units):

                btn = UnitPortrait(unit_name, icon_path)
                btn.hotkey = hotkey
                btn.clicked.connect(self.handle_click)

                self.group_buttons[hotkey].append(btn)

                grid.addWidget(btn, i // 4, i % 4)

            vbox.addWidget(content)
            layout.addWidget(container)

            header.mousePressEvent = lambda e, hk=hotkey: self.toggle_category(hk)

        layout.addStretch()
        self.setLayout(layout)

    # -------------------------
    # CLICK UNIT
    # -------------------------
    def handle_click(self):
        btn = self.sender()
        hotkey = btn.hotkey
        unit = btn.unit_name

        row, col = self.hotkey_position.get(hotkey, (0, 0))

        # toggle off
        if self.group_selected.get(hotkey) == unit:
            self.remove_from_draft(hotkey, unit)
            return

        # unselect others in same category
        for other in self.group_buttons[hotkey]:
            if other != btn:
                other.setChecked(False)

        self.group_selected[hotkey] = unit

        # replace slot
        if hotkey in self.slot_map:
            old = self.slot_map[hotkey]
            self.draft_grid.removeWidget(old)
            old.deleteLater()

        # add clickable top icon
        icon = DraftIcon(
            hotkey,
            unit,
            btn.icon_path,
            self.remove_from_draft
        )

        self.draft_grid.addWidget(icon, row, col)
        self.slot_map[hotkey] = icon

        self.collapse_category(hotkey)

    # -------------------------
    # REMOVE FROM TOP BAR
    # -------------------------
    def remove_from_draft(self, hotkey, unit_name):

        if hotkey in self.slot_map:
            widget = self.slot_map[hotkey]
            self.draft_grid.removeWidget(widget)
            widget.deleteLater()
            del self.slot_map[hotkey]

        self.group_selected[hotkey] = None

        # uncheck button
        for btn in self.group_buttons[hotkey]:
            if btn.unit_name == unit_name:
                btn.setChecked(False)
                break

        self.expand_category(hotkey)

    # -------------------------
    # CATEGORY CONTROL
    # -------------------------
    def toggle_category(self, hotkey):
        widget = self.category_content.get(hotkey)
        if widget:
            widget.setVisible(not widget.isVisible())

    def collapse_category(self, hotkey):
        widget = self.category_content.get(hotkey)
        if widget:
            widget.setVisible(False)

    def expand_category(self, hotkey):
        widget = self.category_content.get(hotkey)
        if widget:
            widget.setVisible(True)

    def collapse_all_categories(self):
        for w in self.category_content.values():
            w.setVisible(False)

    def expand_all_categories(self):
        for w in self.category_content.values():
            w.setVisible(True)

    # -------------------------
    # RESET
    # -------------------------
    def reset(self):
        # clear top bar
        for w in self.slot_map.values():
            self.draft_grid.removeWidget(w)
            w.deleteLater()

        self.slot_map.clear()
        self.group_selected.clear()

        # uncheck all buttons
        for group in self.group_buttons.values():
            for btn in group:
                btn.setChecked(False)

        # expand everything
        for w in self.category_content.values():
            w.setVisible(True)

    # -------------------------
    # COLORS
    # -------------------------
    def get_hotkey_color(self, hotkey):
        colors = {
            "Q": "#2E86AB",
            "W": "#F18F01",
            "E": "#C73E1D",
            "R": "#6A4C93",
            "A": "#2A9D8F",
            "S": "#E76F51",
            "D": "#264653",
            "F": "#8AB17D",
            "Z": "#577590",
            "X": "#F94144",
            "C": "#43AA8B",
        }
        return colors.get(hotkey, "#444444")


# -------------------------
# MAIN UI
# -------------------------
class DraftTrackerUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Direct Strike Draft Tracker")

        # your required default size
        self.setMinimumSize(1100, 800)

        main = QVBoxLayout()

        # -------------------------
        # RESET BUTTON
        # -------------------------
        reset_btn = QPushButton("RESET GAME")
        reset_btn.setFixedHeight(32)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #aa3333;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #cc4444;
            }
        """)
        main.addWidget(reset_btn)

        # -------------------------
        # title
        # -------------------------
        title = QLabel("Enemy Draft Tracker")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        main.addWidget(title)

        # -------------------------
        # enemy panels
        # -------------------------
        row = QWidget()
        row_layout = QHBoxLayout(row)

        self.enemy_panels = [
            EnemyPanel("Enemy 1"),
            EnemyPanel("Enemy 2"),
            EnemyPanel("Enemy 3"),
        ]

        for p in self.enemy_panels:
            row_layout.addWidget(p)

        scroll = QScrollArea()
        scroll.setWidget(row)
        scroll.setWidgetResizable(True)

        main.addWidget(scroll)

        self.setLayout(main)

        reset_btn.clicked.connect(self.reset_all)

    def reset_all(self):
        for panel in self.enemy_panels:
            panel.reset()