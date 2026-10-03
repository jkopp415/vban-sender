from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        # Set window properties
        self.setWindowTitle("VBAN Sender")
        self.resize(QSize(1200, 800))

        # Set app stylesheet
        try:
            with open("src/style.qss", "r") as f:
                styles = f.read()
            self.setStyleSheet(styles)
        except FileNotFoundError:
            print("Stylesheet file 'style.qss' not found.")

        # Set main widget & layout
        # Content widgets will be added to the main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        test_lbl = QLabel(text="Hello!")
        main_layout.addWidget(test_lbl)