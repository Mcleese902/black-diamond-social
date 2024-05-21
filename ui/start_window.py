from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Black Diamond Social")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.loginButton = QPushButton("Login")
        self.loginButton.clicked.connect(self.open_login_window)
        layout.addWidget(self.loginButton)

        self.registerButton = QPushButton("Register")
        self.registerButton.clicked.connect(self.open_register_window)
        layout.addWidget(self.registerButton)

        self.setLayout(layout)

    def open_login_window(self):
        from ui.login_window import LoginWindow  # Local import to avoid circular dependency
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def open_register_window(self):
        from ui.register_window import RegisterWindow  # Local import to avoid circular dependency
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

