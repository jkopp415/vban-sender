from PySide6.QtWidgets import QApplication

from vban_sender.ui.main_window import MainWindow


def run() -> int:
    # TODO: Run a check to make sure the user has PipeWire installed
    app = QApplication([])

    window = MainWindow()
    window.show()

    return app.exec()