import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem,
                             QLabel, QHeaderView, QAbstractItemView, QFrame)
from PyQt6.QtCore import Qt

class NBARosterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2025-26 NBA Roster Stats")
        self.resize(900, 600)
        self.setStyleSheet("background-color: #f4f7f6;") # Main background

        # Main layout wrapper to simulate CSS body padding
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(40, 40, 40, 40)

        # ---------------------------------------------------------
        # 1. Card Container (White background, rounded corners)
        # ---------------------------------------------------------
        self.card = QFrame()
        self.card.setObjectName("Card")
        self.card.setStyleSheet("""
            #Card {
                background-color: #ffffff;
                border-radius: 12px;
            }
        """)
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        self.card_layout.setSpacing(0)

        # ---------------------------------------------------------
        # 2. Header Container (Knicks Blue)
        # ---------------------------------------------------------
        self.header = QFrame()
        self.header.setObjectName("Header")
        self.header.setStyleSheet("""
            #Header {
                background-color: #006bb6;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }
        """)
        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(30, 20, 30, 20)

        # Title Label
        self.title_label = QLabel("New York Knicks (2025-26 Season)")
        self.title_label.setObjectName("Title")
        self.title_label.setStyleSheet("""
            #Title {
                color: white;
                font-size: 22px;
                font-weight: bold;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }
        """)

        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search player name...")
        self.search_input.textChanged.connect(self.filter_table)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: none;
                border-radius: 16px;
                background-color: white;
                color: #333333;
                font-size: 14px;
                min-width: 230px;
            }
            QLineEdit:focus {
                border: 2px solid #f58426; /* Knicks Orange focus ring */
            }
        """)

        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.search_input)

        # ---------------------------------------------------------
        # 3. Data Table
        # ---------------------------------------------------------
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Player", "Pos", "PPG (Points)", "RPG (Rebounds)", "APG (Assists)"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setShowGrid(False)
        
        # Table Styling
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
                font-size: 15px;
                color: #333333;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }
            QTableWidget::item {
                padding: 10px 15px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:selected {
                background-color: #fcfcfc;
                color: #006bb6;
            }
            QHeaderView::section {
                background-color: #f9fafb;
                color: #666666;
                padding: 15px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: bold;
                font-size: 14px;
                text-align: left;
            }
            QHeaderView::section:hover {
                background-color: #f1f3f5;
                color: #006bb6;
            }
        """)

        # Adjust column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, 5):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        self.card_layout.addWidget(self.header)
        self.card_layout.addWidget(self.table)
        self.main_layout.addWidget(self.card)

        self.load_data()

    def load_data(self):
        # Your provided HTML data
        players_data = [
            {"name": "Jalen Brunson", "pos": "PG", "ppg": 26.0, "rpg": 3.3, "apg": 6.8},
            {"name": "Karl-Anthony Towns", "pos": "C", "ppg": 20.1, "rpg": 11.9, "apg": 3.0},
            {"name": "OG Anunoby", "pos": "PF", "ppg": 16.7, "rpg": 5.2, "apg": 2.2},
            {"name": "Mikal Bridges", "pos": "SF", "ppg": 14.4, "rpg": 3.8, "apg": 3.7},
            {"name": "Josh Hart", "pos": "SF", "ppg": 12.0, "rpg": 7.4, "apg": 4.8},
            {"name": "Miles McBride", "pos": "SG", "ppg": 12.0, "rpg": 2.4, "apg": 2.6},
            {"name": "Landry Shamet", "pos": "SG", "ppg": 9.3, "rpg": 1.8, "apg": 1.4},
            {"name": "Mitchell Robinson", "pos": "C", "ppg": 5.7, "rpg": 8.8, "apg": 0.9},
            {"name": "Tyler Kolek", "pos": "PG", "ppg": 4.4, "rpg": 1.6, "apg": 2.7}
        ]

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(players_data))

        for row, player in enumerate(players_data):
            name_item = QTableWidgetItem(player["name"])
            
            pos_item = QTableWidgetItem(player["pos"])
            pos_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Use setData for floats so PyQt natively knows how to sort them numerically
            ppg_item = QTableWidgetItem()
            ppg_item.setData(Qt.ItemDataRole.DisplayRole, player["ppg"])
            
            rpg_item = QTableWidgetItem()
            rpg_item.setData(Qt.ItemDataRole.DisplayRole, player["rpg"])
            
            apg_item = QTableWidgetItem()
            apg_item.setData(Qt.ItemDataRole.DisplayRole, player["apg"])

            # Emphasize player name color to match HTML's .player-name class
            font = name_item.font()
            font.setBold(True)
            name_item.setFont(font)
            name_item.setForeground(Qt.GlobalColor.blue) # Abstracted to standard blue

            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, pos_item)
            self.table.setItem(row, 2, ppg_item)
            self.table.setItem(row, 3, rpg_item)
            self.table.setItem(row, 4, apg_item)

        # Enable clicking headers to sort (PyQt handles the ascending/descending logic automatically)
        self.table.setSortingEnabled(True)

    def filter_table(self, text):
        search_text = text.lower()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0) # Look at the Name column
            if item and search_text in item.text().lower():
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NBARosterApp()
    window.show()
    sys.exit(app.exec())