# main.py

import sys
import requests
import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, \
    QSplitter, QTextEdit
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

import api_clients
import schedule_data


class InfoCard(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("infoCard")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.title_label = QLabel(title)
        self.title_label.setObjectName("cardTitle")
        self.title_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.title_label)
        self.content_widget = None

    def _clear_content(self):
        if self.content_widget:
            self.content_widget.deleteLater()
            self.content_widget = None

    def set_text_content(self, text):
        self._clear_content()
        content_box = QTextEdit()
        content_box.setObjectName("cardContent")
        content_box.setReadOnly(True)
        content_box.setHtml(text)
        self.content_widget = content_box
        self.main_layout.addWidget(self.content_widget)

    def set_image_content(self, pixmap):
        self._clear_content()
        image_label = QLabel()
        image_label.setObjectName("cardContent")
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        self.content_widget = image_label
        self.main_layout.addWidget(self.content_widget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Dashboard")
        self.setGeometry(0, 0, 1600, 900)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(self.splitter)

        self.populate_dashboard_layout()
        self.populate_dashboard_data()

        self.activity_timer = QTimer(self)
        self.activity_timer.timeout.connect(self.update_current_activity)
        self.activity_timer.start(1000)

    def populate_dashboard_layout(self):
        left_column_container = QWidget()
        left_vbox_layout = QVBoxLayout(left_column_container)

        self.activity_card = InfoCard("Current Activity")
        self.quote_card = InfoCard("Quote of the Day")
        self.recipe_card = InfoCard("Recipe of the Day")
        self.calendar_card = InfoCard("Upcoming Events")

        left_vbox_layout.addWidget(self.activity_card, stretch=3)
        left_vbox_layout.addWidget(self.quote_card, stretch=1)
        left_vbox_layout.addWidget(self.recipe_card, stretch=4)
        left_vbox_layout.addWidget(self.calendar_card, stretch=2)

        self.humor_card = InfoCard("Daily Dose of Humor")

        self.splitter.addWidget(left_column_container)
        self.splitter.addWidget(self.humor_card)
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        self.splitter.setSizes([self.width() // 2, self.width() // 2])

    def populate_dashboard_data(self):
        self.update_quote_card()
        self.update_recipe_card()
        self.update_calendar_card()
        self.update_humor_card()
        self.update_current_activity()

    def update_current_activity(self):
        now = datetime.datetime.now()
        day_of_week = now.weekday()

        if day_of_week == 2:
            day_type = "wednesday"
        elif 0 <= day_of_week <= 4:
            day_type = "weekday"
        else:
            day_type = "weekend"

        schedule = schedule_data.DAILY_SCHEDULE[day_type]

        current_activity = "Unscheduled Time"
        current_description = "Flexible time for tasks or relaxation."

        for block in schedule:
            start_time = datetime.datetime.strptime(block["start"], "%H:%M").time()
            end_time = datetime.datetime.strptime(block["end"], "%H:%M").time()
            if start_time <= now.time() < end_time:
                current_activity = block["activity"]
                current_description = block.get("description", "")
                break

        content = f"<b>{current_activity}</b><br>{current_description}"
        self.activity_card.set_text_content(content)

    def update_quote_card(self):
        quote_text = api_clients.fetch_wisdom_quote()
        self.quote_card.set_text_content(quote_text)

    def update_recipe_card(self):
        recipe_data = api_clients.fetch_recipe_of_the_day()
        if recipe_data:
            title = recipe_data.get('title', 'N/A')
            ingredients = recipe_data.get('ingredients', [])
            instructions = recipe_data.get('instructions', 'No instructions provided.')

            formatted_instructions = instructions.replace('\r\n', '<br>').replace('\n', '<br>')

            content = f"<b>{title}</b><br><br><b>Ingredients:</b><br>"
            content += "<br>".join(f"- {ing}" for ing in ingredients)
            content += f"<br><br><b>Instructions:</b><br>{formatted_instructions}"

            self.recipe_card.set_text_content(content)
        else:
            self.recipe_card.set_text_content("Failed to fetch recipe.")

    def update_calendar_card(self):
        events = api_clients.fetch_upcoming_events()
        self.calendar_card.set_text_content("<br><br>".join(events))

    def update_humor_card(self):
        meme_url = api_clients.fetch_trending_meme_url()
        if meme_url:
            try:
                response = requests.get(meme_url, timeout=10)
                response.raise_for_status()
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.humor_card.set_image_content(pixmap)
            except Exception as e:
                self.humor_card.set_text_content(f"Error loading meme: {e}")
        else:
            self.humor_card.set_text_content("Could not fetch meme.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # --- STYLESHEET WITH SCROLLBAR STYLING ---
    app.setStyleSheet("""
        QWidget {
            background-color: #1A1A2E;
            color: #EAEAEA;
            font-family: "Bahnschrift";
            font-size: 15px;
        }
        #infoCard {
            background-color: #1F1F3D;
            border-radius: 8px;
            border: 1px solid #4E4E6A;
        }
        #cardTitle {
            font-size: 20px;
            font-weight: bold;
            color: #00FFFF;
            padding: 10px;
        }
        QSplitter::handle {
            background-color: #4E4E6A;
        }
        QTextEdit {
            background-color: transparent;
            border: none;
            padding: 10px;
            font-size: 15px;
        }

        /* --- THIS IS THE NEW SCROLLBAR STYLING --- */
        QScrollBar:vertical {
            background: #1F1F3D; /* Match the card background */
            width: 15px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #4E4E6A; /* A lighter color for the handle */
            min-height: 20px;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px; /* Hide the top and bottom arrows */
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none; /* Hide the track behind the handle */
        }
    """)
    # --- END OF STYLESHEET ---

    window = MainWindow()
    window.show()
    sys.exit(app.exec())