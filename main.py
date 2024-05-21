import sys
from PyQt5.QtWidgets import QApplication
from ui.start_window import StartWindow
from ui.utils import load_stylesheet  # Adjust the import path as necessary

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Load and apply the QSS stylesheet
    stylesheet = load_stylesheet("assets/styles/dark.qss")
    app.setStyleSheet(stylesheet)

    start_window = StartWindow()
    start_window.show()
    
    sys.exit(app.exec_())

