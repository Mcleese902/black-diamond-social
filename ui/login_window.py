from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
import sqlite3

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Username")
        layout.addWidget(self.usernameInput)

        self.passwordInput = QLineEdit()
        self.passwordInput.setPlaceholderText("Password")
        self.passwordInput.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passwordInput)

        self.loginButton = QPushButton("Login")
        self.loginButton.clicked.connect(self.login_user)
        layout.addWidget(self.loginButton)

        self.setLayout(layout)

    def login_user(self):
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text().strip()

        if username and password:
            connection = sqlite3.connect('black_diamond_social.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            connection.close()
            if user:
                self.hide()
                from ui.main_window import MainWindow  # Local import to avoid circular dependency
                self.main_window = MainWindow(user_id=user[0])
                self.main_window.show()
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password!")
        else:
            QMessageBox.warning(self, "Warning", "Username and password cannot be empty")

