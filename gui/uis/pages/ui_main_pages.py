# ///////////////////////////////////////////////////////////////
#
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# ///////////////////////////////////////////////////////////////

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *
from gui.widgets.py_push_button.py_push_button import PyPushButton
from gui.widgets.py_icon_button.py_icon_button import PyIconButton
from gui.widgets.py_line_edit.py_line_edit import PyLineEdit
from gui.widgets.py_table_widget.py_table_widget import PyTableWidget
from gui.core.functions import Functions
from datetime import datetime
import openpyxl
from PySide6.QtPdf import QPdfDocument
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import fitz
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSizePolicy, QMessageBox
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtGui import QPageSize
from functools import partial
import subprocess
import platform
import os
from sales_manager import SalesManager

class Ui_MainPages(object):

    def setupUi(self, MainPages, themes):
        if themes:
            self.themes = themes
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        
        MainPages.resize(860, 600)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setStyleSheet(u"font-size: 14pt")
        self.page_1_layout = QVBoxLayout(self.page_1)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)

        #self.center_page_layout.addWidget(self.logo)
        self.sales_manager = SalesManager()

        self.sellings_button = PyPushButton("Πωλήσεις",
                                                radius=8,
                                                color=self.themes["app_color"]["text_foreground"],
                                                bg_color=self.themes["app_color"]["dark_three"],
                                                bg_color_hover=self.themes["app_color"]["dark_four"],
                                                bg_color_pressed=self.themes["app_color"]["bg_five"]
                                            )
        icon_size = QSize(60, 60)  # Set the desired size of the icon

        # Load the SVG icon and set its size
        svg_path = "draw-screenshot-icon.svg"
        icon_image = QImage(Functions.set_svg_icon(svg_path))
        icon_pixmap = QPixmap.fromImage(icon_image).scaled(icon_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # Set the icon to the QPushButton
        self.sellings_button.setIcon(QIcon(icon_pixmap))

        self.sellings_button.setFixedHeight(160)
        self.sellings_button.setFixedWidth(400)

        self.sellings_button.clicked.connect(self.handle_sellings_button)

        self.returns_button = PyPushButton("Επιστροφές",
                                                radius=8,
                                                color=self.themes["app_color"]["text_foreground"],
                                                bg_color=self.themes["app_color"]["dark_three"],
                                                bg_color_hover=self.themes["app_color"]["dark_four"],
                                                bg_color_pressed=self.themes["app_color"]["bg_five"]
                                            )
        #self.returns_button.setStyleSheet("font-size: 20px;")
        icon_size = QSize(60, 60)  # Set the desired size of the icon

        # Load the SVG icon and set its size
        svg_path = "pay-money-icon.svg"
        icon_image = QImage(Functions.set_svg_icon(svg_path))
        icon_pixmap = QPixmap.fromImage(icon_image).scaled(icon_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # Set the icon
        self.returns_button.setIcon(QIcon(icon_pixmap))

        self.returns_button.setFixedHeight(160)
        self.returns_button.setFixedWidth(400)

        self.returns_button.clicked.connect(self.handle_returns_button)

        self.exit_button = PyPushButton("Κλείσιμο",
                                                radius=8,
                                                color=self.themes["app_color"]["text_foreground"],
                                                bg_color=self.themes["app_color"]["dark_three"],
                                                bg_color_hover=self.themes["app_color"]["dark_four"],
                                                bg_color_pressed=self.themes["app_color"]["bg_five"]
                                            )
        icon_size = QSize(60, 60)  # Set the desired size of the icon

        # Load the SVG icon and set its size
        svg_path = "icon_close.svg"
        icon_image = QImage(Functions.set_svg_icon(svg_path))
        icon_pixmap = QPixmap.fromImage(icon_image).scaled(icon_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # Set the icon
        self.exit_button.setIcon(QIcon(icon_pixmap))

        self.exit_button.setFixedHeight(80)
        self.exit_button.setFixedWidth(200)

        self.exit_button.clicked.connect(self.handle_exit_button)

        # Spacer above buttons
        self.spacer_above = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Spacer between buttons
        self.spacer_between = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Spacer below buttons
        self.spacer_below = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Adding widgets and spacers to layout
        self.page_1_layout.addItem(self.spacer_above)
        self.page_1_layout.addWidget(self.sellings_button, alignment=Qt.AlignCenter)
        self.page_1_layout.addItem(self.spacer_between)
        self.page_1_layout.addWidget(self.returns_button, alignment=Qt.AlignCenter)
        self.page_1_layout.addItem(self.spacer_below)

        # Layout for the bottom right button
        bottom_right_layout = QVBoxLayout()
        bottom_right_layout.addStretch()
        bottom_right_layout.addWidget(self.exit_button, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.page_1_layout.addLayout(bottom_right_layout)





        # Initialize cost_input here
        self.cost_input = PyLineEdit(place_holder_text="Τιμή",
                                     radius=8,
                                     color=self.themes["app_color"]["text_foreground"],
                                     bg_color=self.themes["app_color"]["dark_one"],
                                     bg_color_active=self.themes["app_color"]["dark_four"]
                                     )
        self.cost_input.setMaximumHeight(40)
        self.cost_input.setFixedWidth(400)
        self.cost_input.setFixedHeight(36)





        self.back_button = PyPushButton("Πίσω",
                                                radius=8,
                                                color=self.themes["app_color"]["text_foreground"],
                                                bg_color=self.themes["app_color"]["dark_three"],
                                                bg_color_hover=self.themes["app_color"]["dark_four"],
                                                bg_color_pressed=self.themes["app_color"]["bg_five"]
                                            )
        icon_size = QSize(60, 60)  # Set the desired size of the icon

        # Load the SVG icon and set its size
        svg_path = "icon_close.svg"
        icon_image = QImage(Functions.set_svg_icon(svg_path))
        icon_pixmap = QPixmap.fromImage(icon_image).scaled(icon_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # Set the icon to the QPushButton
        self.back_button.setIcon(QIcon(icon_pixmap))

        self.back_button.setFixedHeight(80)
        self.back_button.setFixedWidth(200)

        self.back_button.clicked.connect(self.handle_back_button)


        self.pages.addWidget(self.page_1)

        self.main_pages_layout.addWidget(self.pages)

        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))

    def handle_sellings_button(self):
        self.sellings_button.hide()
        self.returns_button.hide()
        self.exit_button.hide()

        # Left side layout for item buttons
        self.left_layout = QVBoxLayout()

        # Helper function to create buttons
        def create_item_button(icon_path, callback):
            if not os.path.exists(icon_path):
                print(f"Icon file '{icon_path}' does not exist.")
                return None
    
            button = PyPushButton(
                "",
                radius=8,
                color=self.themes["app_color"]["text_foreground"],
                bg_color=self.themes["app_color"]["dark_three"],
                bg_color_hover=self.themes["app_color"]["dark_four"],
                bg_color_pressed=self.themes["app_color"]["bg_five"]
            )
            button.setIcon(QIcon(QPixmap(icon_path)))
            button.setIconSize(QSize(64, 64))
            button.setFixedHeight(80)
            button.setFixedWidth(80)
            button.clicked.connect(callback)
            return button
        
        # Get the absolute path of the current file
        current_file_path = os.path.abspath(__file__)

        # Go up three directories
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

        # Define the relative path to the images directory
        images_dir = os.path.join(base_dir, "images/svg_images")

        # Define the absolute paths to the icon files
        dress_icon_path = os.path.join(images_dir, "dress.png")
        skirt_icon_path = os.path.join(images_dir, "skirt.png")
        short_icon_path = os.path.join(images_dir, "shorts.png")
        trouser_icon_path = os.path.join(images_dir, "trouser.png")
        shirt_icon_path = os.path.join(images_dir, "shirt.png")
        t_shirt_icon_path = os.path.join(images_dir, "t-shirt.png")
        blouse_icon_path = os.path.join(images_dir, "blouse.png")
        set_icon_path = os.path.join(images_dir, "clothes.png")
        jacket_icon_path = os.path.join(images_dir, "jacket.png")
        belt_icon_path = os.path.join(images_dir, "belt.png")

        self.dress_button = create_item_button(dress_icon_path, lambda: self.add_item("Φορεμα"))
        self.skirt_button = create_item_button(skirt_icon_path, lambda: self.add_item("Φουστα"))
        self.t_shirt_button = create_item_button(t_shirt_icon_path, lambda: self.add_item("Φανελα"))
        self.blouse_button = create_item_button(blouse_icon_path, lambda: self.add_item("Μπλουζα"))
        self.shirt_button = create_item_button(shirt_icon_path, lambda: self.add_item("Πουκαμισο"))
        self.short_button = create_item_button(short_icon_path, lambda: self.add_item("Σορτσακι"))
        self.trouser_button = create_item_button(trouser_icon_path, lambda: self.add_item("Παντελονι"))
        self.set_button = create_item_button(set_icon_path, lambda: self.add_item("Σετακι"))
        self.jacket_button = create_item_button(jacket_icon_path, lambda: self.add_item("Μπουφαν"))
        self.belt_button = create_item_button(belt_icon_path, lambda: self.add_item("Ζωνη"))

        self.top_layout = QHBoxLayout()

        self.top_layout.addWidget(self.dress_button)
        self.top_layout.addWidget(self.t_shirt_button)
        self.top_layout.addWidget(self.blouse_button)
        self.top_layout.addWidget(self.short_button)
        self.top_layout.addWidget(self.trouser_button)


        self.layout = QHBoxLayout()

        self.layout.addWidget(self.set_button)
        self.layout.addWidget(self.skirt_button)
        self.layout.addWidget(self.shirt_button)
        self.layout.addWidget(self.jacket_button)
        self.layout.addWidget(self.belt_button)
        self.layout.addStretch()

        self.left_layout.addLayout(self.top_layout)
        self.left_layout.addLayout(self.layout)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)

        # Middle section for quantity selection
        self.middle_layout = QVBoxLayout()
        self.middle_layout.setSpacing(0)  # Reduce spacing between widgets
        self.middle_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Quantity selection
        quantity_label = QLabel("ΠΟΣΟΤΗΤΑ")
        self.middle_layout.addWidget(quantity_label, alignment=Qt.AlignCenter)

        vertical_spacer2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.middle_layout.addItem(vertical_spacer2)

        self.quantity_input = PyLineEdit(place_holder_text="Ποσότητα",
                                        radius=8,
                                        color=self.themes["app_color"]["text_foreground"],
                                        bg_color=self.themes["app_color"]["dark_one"],
                                        bg_color_active=self.themes["app_color"]["dark_four"]
                                        )
        self.quantity_input.setMaximumHeight(40)
        self.quantity_input.setFixedWidth(200)
        self.quantity_input.setFixedHeight(36)
        self.quantity_input.setReadOnly(True)

        # Create button group for number buttons
        self.number_button_group = QButtonGroup()
        self.number_button_group.buttonClicked.connect(self.handle_number_button_clicked)

        # Create radio buttons for numbers 1 to 6
        button_layout = QVBoxLayout()
        for i in range(1, 7):
            button = QRadioButton(str(i))
            self.number_button_group.addButton(button, i)
            button_layout.addWidget(button, alignment=Qt.AlignCenter)
            button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add radio button for 'Other'
        self.other_button = QRadioButton("Άλλο:")
        self.other_button.toggled.connect(self.handle_other_button_toggled)

        button_layout.addWidget(self.other_button, alignment=Qt.AlignCenter)

        self.middle_layout.addLayout(button_layout)
        self.middle_layout.addWidget(self.quantity_input, alignment=Qt.AlignLeft)

        # Second separator line (vertical)
        line2 = QFrame()
        line2.setFrameShape(QFrame.VLine)
        line2.setFrameShadow(QFrame.Sunken)

        font2 = QFont()
        font2.setPointSize(40)

        # Add vertical spacer
        vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.middle_layout.addItem(vertical_spacer)

        self.cost_lable = QLabel("ΤΙΜΗ")
        self.cost_lable.setObjectName(u"empty_page_label")
        self.cost_lable.setFont(font2)
        self.cost_lable.setStyleSheet(u"font-size: 10pt")
        self.cost_lable.setAlignment(Qt.AlignLeft)
        self.middle_layout.addWidget(self.cost_lable, alignment=Qt.AlignLeft)

        vertical_spacer2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.middle_layout.addItem(vertical_spacer2)

        self.cost_input = PyLineEdit(place_holder_text="Τιμή",
                                    radius=8,
                                    color=self.themes["app_color"]["text_foreground"],
                                    bg_color=self.themes["app_color"]["dark_one"],
                                    bg_color_active=self.themes["app_color"]["dark_four"]
                                    )
        self.cost_input.setMaximumHeight(40)
        self.cost_input.setFixedWidth(200)
        self.cost_input.setFixedHeight(36)
        self.middle_layout.addWidget(self.cost_input, alignment=Qt.AlignLeft)

        # Right side layout for item list and total
        self.right_layout = QVBoxLayout()

        self.table_widget = PyTableWidget(
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["context_color"],
            bg_color=self.themes["app_color"]["bg_two"],
            header_horizontal_color=self.themes["app_color"]["dark_two"],
            header_vertical_color=self.themes["app_color"]["bg_three"],
            bottom_line_color=self.themes["app_color"]["bg_three"],
            grid_line_color=self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color=self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color=self.themes["app_color"]["dark_four"],
            context_color=self.themes["app_color"]["context_color"]
        )
        font = QFont()
        font.setPointSize(20)  # Adjust the size as needed

        self.table_widget.setFont(font)

        self.right_layout.addWidget(self.table_widget)

        self.total_label = QLabel("Σύνολο: ")
        self.right_layout.addWidget(self.total_label, alignment=Qt.AlignRight)
        self.total_label.setFont(font)

        self.remove_button = PyPushButton("Αφαίρεση",
                                                radius=8,
                                                color=self.themes["app_color"]["white"],
                                                bg_color=self.themes["app_color"]["red"],
                                                bg_color_hover=self.themes["app_color"]["red"],
                                                bg_color_pressed=self.themes["app_color"]["bg_five"]
                                            )
        self.remove_button.setFixedHeight(40)
        self.remove_button.setFixedWidth(100)

        self.remove_button.clicked.connect(self.remove_item)
        self.right_layout.addWidget(self.remove_button, alignment=Qt.AlignRight)

        self.print_button = PyPushButton("Εκτύπωση",
                                                radius=8,
                                                color=self.themes["app_color"]["text_foreground"],
                                                bg_color=self.themes["app_color"]["green"],
                                                bg_color_hover=self.themes["app_color"]["green"],
                                                bg_color_pressed=self.themes["app_color"]["bg_five"]
                                            )
        self.print_button.setFixedHeight(80)
        self.print_button.setFixedWidth(200)

        self.print_button.clicked.connect(self.generate_receipt)
        self.right_layout.addWidget(self.print_button, alignment=Qt.AlignRight)

        # Adding layouts to the main sellings layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(self.left_layout)
        main_layout.addWidget(line2)
        main_layout.addLayout(self.middle_layout)
        main_layout.addWidget(line)
        main_layout.addLayout(self.right_layout)

        self.page_1_layout.addLayout(main_layout)

        self.page_1_layout.addWidget(self.back_button, alignment=Qt.AlignRight | Qt.AlignBottom)
        self.back_button.show()


    def handle_number_button_clicked(self, button):
        self.quantity_input.setText(button.text())
        self.other_button.setChecked(False)  # Uncheck 'Other' button

    def handle_other_button_toggled(self, checked):
        if checked:
            self.quantity_input.clear()
            self.quantity_input.setReadOnly(False)
            self.quantity_input.setFocus()  # Set focus for typing

            # Disconnect number buttons
            self.number_button_group.buttonClicked.disconnect(self.handle_number_button_clicked)
        else:
            self.quantity_input.setReadOnly(True)
            self.number_button_group.buttonClicked.connect(self.handle_number_button_clicked)

    def add_item(self, item):
        quantity = self.quantity_input.text().strip()
        cost = self.cost_input.text().strip()

        if quantity and item and cost:
            try:
                quantity_int = int(quantity)
                cost_float = float(cost)

                row_count = self.table_widget.rowCount()
                self.table_widget.insertRow(row_count)
                self.table_widget.setItem(row_count, 0, QTableWidgetItem(quantity))
                self.table_widget.setItem(row_count, 1, QTableWidgetItem(item))
                self.table_widget.setItem(row_count, 2, QTableWidgetItem(f"€{cost}"))

                # Calculate and update the total after adding the item
                self.calculate_total()
            except ValueError:
                QMessageBox.warning(self.page_1, "Invalid Input", " Παρακαλώ υποβάλετε αρίθμους για ποσότητα και τιμή.")
                self.quantity_input.setFocus()
                return
        else:
            # Display a message box indicating missing input
            QMessageBox.warning(self.page_1, "Missing Input", "Παρακαλώ συμπληρώστε όλα τα στοιχεία (Ποσότητα, Αντικείμενο, Τιμή) προτού υποβληθεί.")

            # Set focus to the quantity input for quick correction
            self.quantity_input.setFocus()

    def remove_item(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self.page_1, "Warning", "Παρακαλώ επιλέξτε τουλάχιστον ένα αντικείμενο για αφαίρεση.")
            return

        for index in sorted(selected_rows, reverse=True):
            self.table_widget.removeRow(index.row())

    def calculate_total(self):
        total = 0
        for row in range(self.table_widget.rowCount()):
            quantity_item = self.table_widget.item(row, 0)  # Assuming the quantity is in the first column (index 0)
            cost_item = self.table_widget.item(row, 2)  # Assuming the cost is in the third column (index 2)
            if quantity_item and cost_item:
                quantity_text = quantity_item.text().strip()
                cost_text = cost_item.text().replace('€', '').strip()
                try:
                    quantity = int(quantity_text)
                    cost = float(cost_text)
                    total += quantity * cost
                except ValueError:
                    pass  # Handle the error if the text cannot be converted to int or float
        
        self.total_label.setText(f"Σύνολο: €{total:.2f}")
        font = QFont()
        font.setPointSize(16)
        self.total_label.setFont(font)

    def handle_returns_button(self):
        self.sellings_button.hide()
        self.returns_button.hide()
        self.exit_button.hide()

        buttons_layout = QVBoxLayout()
        self.page_1_layout.addLayout(buttons_layout, Qt.AlignCenter)

        self.exchange_button = PyPushButton("Αλλαγή",
                                                radius=8,
                                                color=self.themes["app_color"]["text_foreground"],
                                                bg_color=self.themes["app_color"]["dark_three"],
                                                bg_color_hover=self.themes["app_color"]["dark_four"],
                                                bg_color_pressed=self.themes["app_color"]["bg_five"]
                                            )
        icon_size = QSize(60, 60)  # Set the desired size of the icon

        # Load the SVG icon and set its size
        svg_path = "bank-transfer-icon.svg"
        icon_image = QImage(Functions.set_svg_icon(svg_path))
        icon_pixmap = QPixmap.fromImage(icon_image).scaled(icon_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # Set the icon
        self.exchange_button.setIcon(QIcon(icon_pixmap))

        self.exchange_button.setFixedHeight(80)
        self.exchange_button.setFixedWidth(200)

        self.exchange_button.clicked.connect(self.handle_exchange_button)

        buttons_layout.addWidget(self.exchange_button)
        self.page_1_layout.addWidget(self.back_button)
        self.back_button.show()

    def handle_back_button(self):
        # Clear the layout
        while self.page_1_layout.count():
            child = self.page_1_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
            elif child.layout():
                while child.layout().count():
                    sub_child = child.layout().takeAt(0)
                    if sub_child.widget():
                        sub_child.widget().setParent(None)
                    elif sub_child.layout():
                        sub_child.layout().deleteLater()
                child.layout().deleteLater()
            
        # Clear existing layout content
        self.clear_layout(self.middle_layout)
        self.clear_layout(self.left_layout)
        self.clear_layout(self.right_layout)
        
        # Adding widgets and spacers to layout
        self.page_1_layout.addItem(self.spacer_above)
        self.page_1_layout.addWidget(self.sellings_button, alignment=Qt.AlignCenter)
        self.page_1_layout.addItem(self.spacer_between)
        self.page_1_layout.addWidget(self.returns_button, alignment=Qt.AlignCenter)
        self.page_1_layout.addItem(self.spacer_below)

        # Layout for the bottom right button
        bottom_right_layout = QVBoxLayout()
        bottom_right_layout.addStretch()
        bottom_right_layout.addWidget(self.exit_button, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.page_1_layout.addLayout(bottom_right_layout)
        
        # Show the buttons again
        self.sellings_button.show()
        self.returns_button.show()
        self.exit_button.show()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def handle_exit_button(self):
        """Exit the application."""
        QApplication.instance().quit()







    def generate_receipt(self):
        if self.table_widget:
            self.invoice_number = self.sales_manager.get_next_invoice_number()
            # Generate the PDF receipt
            self.generate_pdf_receipt()

            # Print the PDF receipt
            self.print_receipt()
        else:
            pass

    def generate_pdf_receipt(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.pdf_filename = f"{current_datetime}_receipt.pdf"

        c = canvas.Canvas(self.pdf_filename, pagesize=letter)
        c.setFont("Times-Bold", 14)
        
        line_height = 14
        y_position = 760
        
        # Header
        c.drawString(280, y_position, "Fancy Shop")
        y_position -= line_height * 4

        c.drawString(50, y_position, current_datetime)
        y_position -= line_height * 2

        c.drawString(50, y_position, f"Invoice Number: {self.invoice_number}")
        y_position -= line_height * 2

        c.drawString(50, y_position, f"Address:")
        y_position -= line_height * 2

        c.drawString(50, y_position, f"Telephone:")
        y_position -= line_height * 2

        c.drawString(50, y_position, f"Email:")
        y_position -= line_height * 2

        c.drawString(50, y_position, f"VAT ID:")
        y_position -= line_height * 2

        c.drawString(50, y_position, f"TAX ID:")
        y_position -= line_height * 4
        
        # Column headers
        c.setFont("Times-Bold", 12)
        c.drawString(80, y_position, "CODE")
        c.drawString(210, y_position, "Description")
        c.drawString(360, y_position, "Qty")
        c.drawString(460, y_position, "Amount")
        y_position -= line_height * 2
        c.setFont("Times-Roman", 12)

        # Assuming self.total_label.text() returns something like "Total: €123.45"
        total_text = self.total_label.text().strip()

        # Find the index of '£' in the text
        index_of_pound = total_text.find('€')

        if index_of_pound != -1:  # Check if '€' is found
            # Extract the substring after '€'
            total_value = total_text[index_of_pound + 1:].strip()
            print(total_value)  # This will print "123.45" assuming "Total: £123.45"
        else:
            print("€ not found in total_label text")
        
        total_profit = 0
        total_VAT = 0

        # Items details
        for row in range(self.table_widget.rowCount()):
            # Check if QTableWidgetItem exists before accessing text
            quantity_item = self.table_widget.item(row, 0)
            item_name_item = self.table_widget.item(row, 1)
            cost_item = self.table_widget.item(row, 2)

            if quantity_item and item_name_item and cost_item:
                cost_text = cost_item.text().strip().replace('€', '')

                cost_value = float(cost_text)  # Convert the text to a float
                cost_value_with_VAT = cost_value / 1.19
                quantity = quantity_item.text()
                item_name = item_name_item.text()

                product_codes = self.sales_manager.record_sale(self.invoice_number, item_name.lower(), int(quantity), cost_value)

                # Join product codes with a slash
                product_codes_str = "/".join(product_codes)

                c.drawString(80, y_position, product_codes_str)  # Convert row_number to string
                c.drawString(220, y_position, item_name)
                c.drawString(370, y_position, quantity)
                c.drawString(465, y_position, f"€{cost_value_with_VAT*float(quantity):.2f}")

                total_profit += cost_value_with_VAT * int(quantity)
                
                y_position -= line_height
        
        total_VAT = (float(total_value) - total_profit)

        # Totals section
        y_position -= line_height * 2

        c.setFont("Times-Bold", 12)
        c.drawString(270, y_position, "_______________________________________")
        y_position -= line_height

        c.drawString(270, y_position, "ΣΥΝΟΛΟ")
        c.setFont("Times-Roman", 12)

        c.drawString(465, y_position, f"€{total_profit:.2f}")
        y_position -= line_height
        
        c.setFont("Times-Bold", 12)
        c.drawString(270, y_position, "ΦΠΑ")
        c.setFont("Times-Roman", 12)
        c.drawString(465, y_position, f"€{total_VAT:.2f}")
        y_position -= line_height
            
        c.setFont("Times-Bold", 12)
        c.drawString(270, y_position, "ΟΛΙΚΟ")
        c.setFont("Times-Roman", 12)
        c.drawString(465, y_position, f"€{total_value}")
        
        c.save()

        print(f"{'PDF receipt'} '{self.pdf_filename}' {'generated successfully.'}")

        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

        total_profit = 0
        total_VAT = 0

    def print_receipt(self):
        pdf_filename = self.pdf_filename

        try:
            if platform.system() == 'Darwin':  # macOS
                print("CORRECT OPERATING SYSTEM")
                subprocess.run(["lp", "-n", "2", pdf_filename], check=True)
                print(f"PDF '{pdf_filename}' sent to printer successfully.")
            elif platform.system() == 'Windows':
                # Assuming you have Acrobat Reader or Foxit Reader installed
                for _ in range(2):  # Print twice
                    subprocess.run(["cmd", "/c", "start", "/min", "AcroRd32.exe", "/t", pdf_filename], check=True)
                print(f"PDF '{pdf_filename}' sent to printer successfully.")
            else:
                print(f"Unsupported operating system: {platform.system()}. Cannot print PDF.")
        except subprocess.CalledProcessError as e:
            print(f"Error printing PDF '{pdf_filename}': {e}")


    ##def print_receipt(self):
        # Create printer object
        ##printer = QPrinter(QPrinter.HighResolution)

        # Set printer settings
        ##printer.setOutputFormat(QPrinter.OutputFormat.NativeFormat)
        ##printer.setPageSize(QPageSize(QPageSize.A4))

        ##dialog = QPrintDialog(printer)
        ##if dialog.exec_() == QPrintDialog.Accepted:
            # Open the generated PDF file
            ##with open(self.pdf_filename, 'rb') as f:
                ##pdf_content = f.read()

            ##printer.newPage()
            ##painter = QPainter()
            ##painter.begin(printer)

            # Draw the PDF content on the printer
            ##painter.drawText(10, 10, pdf_content)
            ##painter.end()


    def handle_exchange_button(self):
        pass