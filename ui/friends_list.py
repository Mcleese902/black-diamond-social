from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox
import sqlite3

class FriendsList(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Friends List")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()
        self.load_friends()

    def initUI(self):
        layout = QVBoxLayout()

        self.friendsList = QListWidget()
        layout.addWidget(self.friendsList)

        self.addFriendButton = QPushButton("Add Friend")
        self.addFriendButton.clicked.connect(self.add_friend)
        layout.addWidget(self.addFriendButton)

        self.setLayout(layout)

    def load_friends(self):
        connection = sqlite3.connect('black_diamond_social.db')
        cursor = connection.cursor()
        cursor.execute("""
            SELECT u.username 
            FROM friends f
            JOIN users u ON f.friend_id = u.id
            WHERE f.user_id = ? AND f.status = 'accepted'
        """, (self.user_id,))
        friends = cursor.fetchall()
        connection.close()
        
        self.friendsList.clear()
        for friend in friends:
            self.friendsList.addItem(friend[0])

    def add_friend(self):
        friend_username, ok = QInputDialog.getText(self, 'Add Friend', 'Enter friend\'s username:')
        if ok and friend_username:
            connection = sqlite3.connect('black_diamond_social.db')
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (friend_username,))
            friend = cursor.fetchone()
            if friend:
                friend_id = friend[0]
                cursor.execute("INSERT INTO friends (user_id, friend_id, status) VALUES (?, ?, 'pending')", (self.user_id, friend_id))
                connection.commit()
                QMessageBox.information(self, 'Success', 'Friend request sent!')
            else:
                QMessageBox.warning(self, 'Error', 'User not found')
            connection.close()

