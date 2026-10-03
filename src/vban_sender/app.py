from PySide6.QtWidgets import QApplication

from vban_sender.ui.main_window import MainWindow


def run() -> int:
    app = QApplication([])

    window = MainWindow()
    window.show()

    return app.exec()