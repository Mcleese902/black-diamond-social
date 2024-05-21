from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit
import sqlite3

class UserProfile(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("User Profile")
        self.setGeometry(100, 100, 400, 400)
        self.initUI()
        self.load_profile()

    def initUI(self):
        layout = QVBoxLayout()

        self.profilePictureLabel = QLabel("Profile Picture:")
        layout.addWidget(self.profilePictureLabel)
        
        self.profilePictureInput = QLineEdit()
        layout.addWidget(self.profilePictureInput)

        self.bioLabel = QLabel("Bio:")
        layout.addWidget(self.bioLabel)

        self.bioInput = QTextEdit()
        layout.addWidget(self.bioInput)

        self.signatureLabel = QLabel("Signature:")
        layout.addWidget(self.signatureLabel)

        self.signatureInput = QLineEdit()
        layout.addWidget(self.signatureInput)

        self.socialLinksLabel = QLabel("Social Links:")
        layout.addWidget(self.socialLinksLabel)

        self.socialLinksInput = QTextEdit()
        layout.addWidget(self.socialLinksInput)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save_profile)
        layout.addWidget(self.saveButton)

        self.setLayout(layout)

    def load_profile(self):
        connection = sqlite3.connect('black_diamond_social.db')
        cursor = connection.cursor()
        cursor.execute("SELECT profile_picture, bio, signature, social_links FROM user_profiles WHERE user_id = ?", (self.user_id,))
        profile = cursor.fetchone()
        connection.close()
        if profile:
            self.profilePictureInput.setText(profile[0])
            self.bioInput.setPlainText(profile[1])
            self.signatureInput.setText(profile[2])
            self.socialLinksInput.setPlainText(profile[3])

    def save_profile(self):
        profile_picture = self.profilePictureInput.text().strip()
        bio = self.bioInput.toPlainText().strip()
        signature = self.signatureInput.text().strip()
        social_links = self.socialLinksInput.toPlainText().strip()

        connection = sqlite3.connect('black_diamond_social.db')
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO user_profiles (user_id, profile_picture, bio, signature, social_links)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                profile_picture=excluded.profile_picture,
                bio=excluded.bio,
                signature=excluded.signature,
                social_links=excluded.social_links
        """, (self.user_id, profile_picture, bio, signature, social_links))
        connection.commit()
        connection.close()
        QMessageBox.information(self, "Success", "Profile updated successfully!")

