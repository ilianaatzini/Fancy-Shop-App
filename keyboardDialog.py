from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

from qt_core import *

class KeyboardDialog(QDialog):
    text_selected = Signal(str)  # Define a signal to emit the selected text

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set dialog properties
        self.setWindowTitle("Virtual Keyboard")
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #E0E0E0;")

        # Layout for the keyboard buttons
        layout = QGridLayout()

        # Define keyboard button texts (0-9 and .)
        button_texts = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']

        # Create example keyboard buttons
        buttons = []
        for i, text in enumerate(button_texts):
            button = QPushButton(text)
            button.setStyleSheet("background-color: #FFFFFF; color: black; font-size: 18px; height: 50px;")
            button.clicked.connect(self.on_button_clicked)
            buttons.append(button)

            # Calculate positions for the grid
            row = i // 4
            col = i % 4
            layout.addWidget(button, row, col)

        # Add back button
        back_button = QPushButton("Διαγραφή")
        back_button.setStyleSheet("background-color: #FFA500; color: #FFFFFF; font-size: 18px; height: 50px;")
        back_button.clicked.connect(self.on_back_button_clicked)
        layout.addWidget(back_button, (len(button_texts) // 4) + 1, 0, 1, 4)  # Place the back button in the next row
        
        # Add close button
        close_button = QPushButton("Κλείσιμο")
        close_button.setStyleSheet("background-color: #FF0000; color: #FFFFFF; font-size: 18px; height: 50px;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, (len(button_texts) // 4) + 2, 0, 1, 4)  # Span close button across the bottom row

        # Set layout for the dialog
        self.setLayout(layout)

        # Initialize selected text attribute
        self.selected_text = ""

    def on_button_clicked(self):
        # Handle button clicks here (e.g., emit signal with selected text)
        button = self.sender()
        if isinstance(button, QPushButton):
            self.selected_text += button.text()
            self.text_selected.emit(self.selected_text)  # Emit signal with selected text

    def on_back_button_clicked(self):
        # Handle back button click to remove the last character
        if self.selected_text:
            self.selected_text = self.selected_text[:-1]
            self.text_selected.emit(self.selected_text)  # Emit signal with updated text