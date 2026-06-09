import os
import sys
from unittest import result

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLabel,
    QScrollArea,
    QPushButton, QGridLayout,
    QApplication
)

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt
from torch import layout
from damage_analysis import analyze_armor_profile, analyze_attack_profile

from units import UNITS_BY_HOTKEY


# -------------------------
# PATH HELPER (EXE SAFE)
# -------------------------
def asset_path(path):
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base, path)


# -------------------------
# TOP DRAFT ICON (CLICK TO REMOVE)
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


#
# Segmented Bar for Armor and Attack distribution
#

class SegmentedBar(QWidget):

    ARMOR_LABELS = {
        "Heavy": "H",
        "Medium": "M",
        "Light": "L",
        "Unarmored": "U",
        "Fortified": "F",
    }

    ATTACK_LABELS = {
        "Normal": "N",
        "Pierce": "P",
        "Magic": "MG",
        "Siege": "S",
    }

    COLORS = {
        # Armor
        "Heavy": "#8B4513",
        "Medium": "#3A7BD5",
        "Light": "#43AA8B",
        "Unarmored": "#A855F7",
        "Fortified": "#555555",

        # Attack
        "Normal": "#D97706",
        "Pierce": "#2563EB",
        "Magic": "#9333EA",
        "Siege": "#DC2626",
    }

    def __init__(self, type_counts, mode):
        super().__init__()

        labels = (
            self.ARMOR_LABELS
            if mode == "armor"
            else self.ATTACK_LABELS
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        total = sum(type_counts.values())

        if total == 0:
            self.setLayout(layout)
            return

        for type_name, count in type_counts.items():

            percent = round((count / total) * 100)

            segment = QLabel(
                f"{labels.get(type_name, type_name)} {percent}%"
            )

            segment.setAlignment(Qt.AlignCenter)

            segment.setStyleSheet(f"""
                QLabel {{
                    background-color: {self.COLORS.get(type_name, "#444444")};
                    color: white;
                    font-weight: bold;
                    padding: 4px;
                    border-radius: 3px;
                }}
            """)

            layout.addWidget(segment, count)

        self.setLayout(layout)


# -------------------------
# UNIT BUTTON
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
# ENEMY PANEL
# -------------------------
class EnemyPanel(QGroupBox):


    # Updating info for player based ona armor and attacktypes of selected units
    def update_analysis(self):
        armor = analyze_armor_profile(self.group_selected)
        attack = analyze_attack_profile(self.group_selected)

        self.clear_layout(self.armor_bars_layout)
        self.clear_layout(self.attack_bars_layout)

        # -------------------------
        # Armor profile
        # -------------------------
        if armor["status"] == "unknown":
            self.armor_bars_layout.addWidget(
                QLabel("Armor: unknown")
            )
        else:
            self.armor_bars_layout.addWidget(
                SegmentedBar(
                    armor["armor_counts"],
                    "armor"
                )
            )

            damage = ", ".join(
                armor["recommended_damage"]
            )

            self.armor_bars_layout.addWidget(
                QLabel(f"Build: {damage} Damage")
            )

        # -------------------------
        # Attack profile
        # -------------------------
        if attack["status"] == "unknown":
            self.attack_bars_layout.addWidget(
                QLabel("Attack: unknown")
            )
        else:
            self.attack_bars_layout.addWidget(
                SegmentedBar(
                    attack["attack_counts"],
                    "attack"
                )
            )

            armor_rec = ", ".join(
                attack["recommended_armor"]
            )

            self.attack_bars_layout.addWidget(
                QLabel(f"Build: {armor_rec}")
            )
    

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

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
        # TOP DRAFT BAR
        # -------------------------
        self.draft_grid = QGridLayout()
        self.slot_map = {}
        self.group_selected = {}

        draft_container = QWidget()
        draft_container.setLayout(self.draft_grid)
        draft_container.setFixedHeight(180)

        layout.addWidget(draft_container)

        #
        # Analaysis bars
        #

        self.armor_bars_layout = QVBoxLayout()
        self.attack_bars_layout = QVBoxLayout()

        armor_box = QGroupBox("Armor Profile")
        armor_box.setLayout(self.armor_bars_layout)

        attack_box = QGroupBox("Attack Profile")
        attack_box.setLayout(self.attack_bars_layout)

        layout.addWidget(armor_box)
        layout.addWidget(attack_box)

        # -------------------------
        # STATE
        # -------------------------
        self.group_buttons = {}
        self.category_content = {}

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
        # CATEGORIES
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
                    border-radius: 6px;
                    border: 2px solid #222;
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

        # toggle off
        if self.group_selected.get(hotkey) == unit:
            self.remove_from_draft(hotkey, unit)
            return

        # unselect others in category
        for other in self.group_buttons[hotkey]:
            if other != btn:
                other.setChecked(False)

        self.group_selected[hotkey] = unit

        row, col = self.hotkey_position.get(hotkey, (0, 0))

        # replace slot
        if hotkey in self.slot_map:
            old = self.slot_map[hotkey]
            self.draft_grid.removeWidget(old)
            old.deleteLater()

        icon = DraftIcon(
            hotkey,
            unit,
            btn.icon_path,
            self.remove_from_draft
        )

        self.draft_grid.addWidget(icon, row, col)
        self.slot_map[hotkey] = icon

        self.collapse_category(hotkey)
        self.update_analysis()

    # -------------------------
    # REMOVE FROM TOP
    # -------------------------
    def remove_from_draft(self, hotkey, unit_name):

        if hotkey in self.slot_map:
            widget = self.slot_map[hotkey]
            self.draft_grid.removeWidget(widget)
            widget.deleteLater()
            del self.slot_map[hotkey]

        self.group_selected[hotkey] = None

        for btn in self.group_buttons[hotkey]:
            if btn.unit_name == unit_name:
                btn.setChecked(False)
                break

        self.expand_category(hotkey)
        self.update_analysis()

    # -------------------------
    # CATEGORY TOGGLES
    # -------------------------
    def toggle_category(self, hotkey):
        w = self.category_content.get(hotkey)
        if w:
            w.setVisible(not w.isVisible())

    def collapse_category(self, hotkey):
        w = self.category_content.get(hotkey)
        if w:
            w.setVisible(False)

    def expand_category(self, hotkey):
        w = self.category_content.get(hotkey)
        if w:
            w.setVisible(True)

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
        for w in self.slot_map.values():
            self.draft_grid.removeWidget(w)
            w.deleteLater()

        self.slot_map.clear()
        self.group_selected.clear()

        for group in self.group_buttons.values():
            for btn in group:
                btn.setChecked(False)

        for w in self.category_content.values():
            w.setVisible(True)
        self.update_analysis()

    #Parser for selecting units by name (used by command popup)
    def select_unit_by_name(self, unit_name):
        target = unit_name.lower()

        for hotkey, buttons in self.group_buttons.items():
            for btn in buttons:
                if btn.unit_name.lower() == target:
                    if not btn.isChecked():
                        btn.click()
                    return True

        print(f"[WARN] Unit not found: {unit_name}")
        return False
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
        return colors.get(hotkey, "#444")


# -------------------------
# MAIN WINDOW
# -------------------------
class DraftTrackerUI(QWidget):
    def __init__(self):
        from PySide6.QtGui import QIcon
        super().__init__()

        self.setWindowTitle("Direct Strike Tracker")
        self.setWindowIcon(QIcon("icons/logo.ico"))
        # IMPORTANT: fixes taskbar + proper window behavior
        self.setWindowFlags(Qt.Window)
        self.setMinimumSize(1100, 800)

        main = QVBoxLayout()

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

        title = QLabel("Made by Horiciculic and Nemo")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        main.addWidget(title)

        row = QWidget()
        row_layout = QHBoxLayout(row)

        self.enemy_panels = [
            EnemyPanel("TOP ENEMY"),
            EnemyPanel("MIDDLE ENEMY"),
            EnemyPanel("BOTTOM ENEMY"),
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
        for p in self.enemy_panels:
            p.reset()

    def closeEvent(self, event):
        QApplication.instance().quit()
        event.accept()