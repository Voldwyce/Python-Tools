import sys
import random
import datetime
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

# List of quotes
quotes = [
    "The best way to predict the future is to invent it. - Alan Kay",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "If you want to lift yourself up, lift up someone else. - Booker T. Washington"
]

class QuoteApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.setWindowTitle("Quote of the Day")
        self.setGeometry(100, 100, 400, 200)

        # Create layout
        layout = QVBoxLayout()

        # Create and set up widgets
        self.quote_label = QLabel("", self)
        self.date_label = QLabel("", self)
        self.new_quote_button = QPushButton("New Quote", self)

        # Add widgets to layout
        layout.addWidget(self.quote_label)
        layout.addWidget(self.date_label)
        layout.addWidget(self.new_quote_button)

        # Set layout
        self.setLayout(layout)

        # Connect button click to function
        self.new_quote_button.clicked.connect(self.display_quote)

        # Display the first quote
        self.display_quote()

    def display_quote(self):
        # Select a random quote
        quote = random.choice(quotes)
        # Get the current date
        date = datetime.date.today()
        # Update labels
        self.quote_label.setText(quote)
        self.date_label.setText(f"- {date}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuoteApp()
    window.show()
    sys.exit(app.exec())
