from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
import sqlite3

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
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

        self.registerButton = QPushButton("Register")
        self.registerButton.clicked.connect(self.register_user)
        layout.addWidget(self.registerButton)

        self.setLayout(layout)

    def register_user(self):
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text().strip()

        if username and password:
            connection = sqlite3.connect('black_diamond_social.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Error", "Username already taken!")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                connection.commit()
                connection.close()
                QMessageBox.information(self, "Success", "Registration successful!")
                self.close()
                from ui.login_window import LoginWindow  # Local import to avoid circular dependency
                self.login_window = LoginWindow()
                self.login_window.show()
        else:
            QMessageBox.warning(self, "Warning", "Username and password cannot be empty")

