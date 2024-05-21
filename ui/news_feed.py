from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QListWidget, QMessageBox
import sqlite3

class NewsFeed(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("News Feed")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()
        self.load_status_updates()

    def initUI(self):
        layout = QVBoxLayout()

        self.statusInput = QTextEdit()
        self.statusInput.setPlaceholderText("What's on your mind?")
        layout.addWidget(self.statusInput)

        self.postButton = QPushButton("Post")
        self.postButton.clicked.connect(self.post_status)
        layout.addWidget(self.postButton)

        self.statusList = QListWidget()
        layout.addWidget(QLabel("Recent Updates:"))
        layout.addWidget(self.statusList)

        self.setLayout(layout)

    def post_status(self):
        status = self.statusInput.toPlainText().strip()
        if status:
            connection = sqlite3.connect('black_diamond_social.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO status_updates (user_id, content) VALUES (?, ?)", (self.user_id, status))
            connection.commit()
            connection.close()
            self.load_status_updates()
            self.statusInput.clear()
        else:
            QMessageBox.warning(self, "Warning", "Status cannot be empty")

    def load_status_updates(self):
        connection = sqlite3.connect('black_diamond_social.db')
        cursor = connection.cursor()
        cursor.execute("""
            SELECT u.username, s.content, s.timestamp 
            FROM status_updates s
            JOIN users u ON s.user_id = u.id
            ORDER BY s.timestamp DESC
        """)
        updates = cursor.fetchall()
        connection.close()
        
        self.statusList.clear()
        for update in updates:
            item = f"{update[0]}: {update[1]} ({update[2]})"
            self.statusList.addItem(item)

