import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem,
                             QLabel, QHeaderView, QAbstractItemView, QFrame, QTabWidget,
                             QGridLayout)
from PyQt6.QtCore import Qt

class NBARosterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2025-26 NBA Roster Stats")
        self.resize(950, 650)
        self.setStyleSheet("background-color: #f4f7f6;") # Main background

        # Main layout wrapper
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
        # 2. Global Header (Knicks Blue)
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
                font-size: 24px;
                font-weight: bold;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }
        """)
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()

        self.card_layout.addWidget(self.header)

        # ---------------------------------------------------------
        # 3. Tab Widget
        # ---------------------------------------------------------
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #ffffff;
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
            }
            QTabBar::tab {
                background-color: #f1f3f5;
                color: #555555;
                padding: 12px 25px;
                font-size: 15px;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
                margin-top: 10px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #006bb6;
                border-bottom: 3px solid #f58426; /* Knicks Orange active indicator */
            }
            QTabBar::tab:hover:!selected {
                background-color: #e9ecef;
            }
        """)

        # Create the individual tabs
        self.setup_roster_tab()
        self.setup_overview_tab()
        self.setup_schedule_tab()

        self.card_layout.addWidget(self.tabs)
        self.main_layout.addWidget(self.card)

    def setup_roster_tab(self):
        """Sets up the original Player Stats tab with the search bar and table."""
        self.roster_tab = QWidget()
        layout = QVBoxLayout(self.roster_tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Search Bar specific to the Roster Tab
        search_layout = QHBoxLayout()
        search_layout.addStretch()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search player name...")
        self.search_input.textChanged.connect(self.filter_table)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 1px solid #cccccc;
                border-radius: 18px;
                background-color: #f9fafb;
                color: #333333;
                font-size: 14px;
                min-width: 250px;
            }
            QLineEdit:focus {
                border: 2px solid #f58426;
                background-color: #ffffff;
            }
        """)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Data Table
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
            }
            QTableWidget::item {
                padding: 12px 15px;
                border-bottom: 1px solid #eef0f2;
            }
            QTableWidget::item:selected {
                background-color: #f4f8fb;
                color: #006bb6;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #495057;
                padding: 12px 15px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                font-size: 14px;
                text-align: left;
            }
            QHeaderView::section:hover {
                background-color: #e9ecef;
            }
        """)

        # Adjust column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, 5):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        layout.addWidget(self.table)
        self.load_roster_data()
        self.tabs.addTab(self.roster_tab, "Player Stats")

    def setup_overview_tab(self):
        """Sets up a mock Team Overview tab."""
        self.overview_tab = QWidget()
        layout = QVBoxLayout(self.overview_tab)
        layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel("Season Overview")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #333;")
        
        desc = QLabel("The New York Knicks enter the 2025-26 season with high expectations following major roster moves. Led by Jalen Brunson and Karl-Anthony Towns, the team looks to secure a top seed in the Eastern Conference.")
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 16px; color: #555; line-height: 1.5;")
        
        stats_layout = QGridLayout()
        stats_layout.addWidget(self.create_stat_card("Current Record", "0-0"), 0, 0)
        stats_layout.addWidget(self.create_stat_card("Conference Rank", "T-1st"), 0, 1)
        stats_layout.addWidget(self.create_stat_card("Head Coach", "Tom Thibodeau"), 1, 0)
        stats_layout.addWidget(self.create_stat_card("Arena", "Madison Square Garden"), 1, 1)

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(desc)
        layout.addSpacing(30)
        layout.addLayout(stats_layout)
        layout.addStretch()
        
        self.tabs.addTab(self.overview_tab, "Team Overview")

    def create_stat_card(self, title_text, value_text):
        """Helper to create small stat cards for the Overview tab."""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(frame)
        title = QLabel(title_text)
        title.setStyleSheet("color: #6c757d; font-size: 13px; font-weight: bold; text-transform: uppercase;")
        value = QLabel(value_text)
        value.setStyleSheet("color: #006bb6; font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        layout.addWidget(value)
        return frame

    def setup_schedule_tab(self):
        """Sets up a mock Schedule tab."""
        self.schedule_tab = QWidget()
        layout = QVBoxLayout(self.schedule_tab)
        layout.setContentsMargins(20, 20, 20, 20)

        schedule_table = QTableWidget()
        schedule_table.setColumnCount(4)
        schedule_table.setHorizontalHeaderLabels(["Date", "Opponent", "Location", "Time (EST)"])
        schedule_table.verticalHeader().setVisible(False)
        schedule_table.setShowGrid(False)
        schedule_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        schedule_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        schedule_table.setStyleSheet(self.table.styleSheet()) # Reuse roster table styles
        
        header = schedule_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        games = [
            ("Oct 22, 2025", "vs. Boston Celtics", "Home", "7:30 PM"),
            ("Oct 25, 2025", "@ Philadelphia 76ers", "Away", "8:00 PM"),
            ("Oct 27, 2025", "vs. Miami Heat", "Home", "7:30 PM"),
            ("Oct 29, 2025", "@ Milwaukee Bucks", "Away", "7:00 PM")
        ]

        schedule_table.setRowCount(len(games))
        for row, game in enumerate(games):
            for col, text in enumerate(game):
                item = QTableWidgetItem(text)
                if col == 1 and "vs." in text:
                    item.setForeground(Qt.GlobalColor.blue)
                schedule_table.setItem(row, col, item)

        layout.addWidget(schedule_table)
        self.tabs.addTab(self.schedule_tab, "Upcoming Schedule")

    def load_roster_data(self):
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
            
            ppg_item = QTableWidgetItem()
            ppg_item.setData(Qt.ItemDataRole.DisplayRole, player["ppg"])
            
            rpg_item = QTableWidgetItem()
            rpg_item.setData(Qt.ItemDataRole.DisplayRole, player["rpg"])
            
            apg_item = QTableWidgetItem()
            apg_item.setData(Qt.ItemDataRole.DisplayRole, player["apg"])

            font = name_item.font()
            font.setBold(True)
            name_item.setFont(font)
            name_item.setForeground(Qt.GlobalColor.blue)

            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, pos_item)
            self.table.setItem(row, 2, ppg_item)
            self.table.setItem(row, 3, rpg_item)
            self.table.setItem(row, 4, apg_item)

        self.table.setSortingEnabled(True)

    def filter_table(self, text):
        search_text = text.lower()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and search_text in item.text().lower():
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NBARosterApp()
    window.show()
    sys.exit(app.exec())