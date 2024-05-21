from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox
import sqlite3

class CoworkersList(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Co-Workers List")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()
        self.load_coworkers()

    def initUI(self):
        layout = QVBoxLayout()

        self.coworkersList = QListWidget()
        layout.addWidget(self.coworkersList)

        self.addCoworkerButton = QPushButton("Add Co-Worker")
        self.addCoworkerButton.clicked.connect(self.add_coworker)
        layout.addWidget(self.addCoworkerButton)

        self.setLayout(layout)

    def load_coworkers(self):
        connection = sqlite3.connect('black_diamond_social.db')
        cursor = connection.cursor()
        cursor.execute("""
            SELECT u.username 
            FROM coworkers c
            JOIN users u ON c.coworker_id = u.id
            WHERE c.user_id = ? AND c.status = 'accepted'
        """, (self.user_id,))
        coworkers = cursor.fetchall()
        connection.close()
        
        self.coworkersList.clear()
        for coworker in coworkers:
            self.coworkersList.addItem(coworker[0])

    def add_coworker(self):
        coworker_username, ok = QInputDialog.getText(self, 'Add Co-Worker', 'Enter co-worker\'s username:')
        if ok and coworker_username:
            connection = sqlite3.connect('black_diamond_social.db')
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (coworker_username,))
            coworker = cursor.fetchone()
            if coworker:
                coworker_id = coworker[0]
                cursor.execute("INSERT INTO coworkers (user_id, coworker_id, status) VALUES (?, ?, 'pending')", (self.user_id, coworker_id))
                connection.commit()
                QMessageBox.information(self, 'Success', 'Co-worker request sent!')
            else:
                QMessageBox.warning(self, 'Error', 'User not found')
            connection.close()

