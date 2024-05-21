from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QScrollArea, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDateTime
from llama3_api import get_response, get_response_stream

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat with Llama3")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Chat history area
        self.chatHistory = QTextEdit()
        self.chatHistory.setReadOnly(True)
        self.chatHistory.setFont(QFont("Arial", 12))
        layout.addWidget(self.chatHistory)

        # Scroll area for chat history
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(self.chatHistory)
        layout.addWidget(scrollArea)

        # Input area
        inputLayout = QHBoxLayout()
        
        self.messageInput = QTextEdit()
        self.messageInput.setFont(QFont("Arial", 12))
        self.messageInput.setPlaceholderText("Type your message here...")
        self.messageInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        inputLayout.addWidget(self.messageInput)

        self.sendButton = QPushButton("Send")
        self.sendButton.setFont(QFont("Arial", 12))
        self.sendButton.clicked.connect(self.send_message)
        inputLayout.addWidget(self.sendButton)

        layout.addLayout(inputLayout)

        self.setLayout(layout)

    def send_message(self):
        message = self.messageInput.toPlainText().strip()
        if message:
            self.append_message("You", message)
            self.messageInput.clear()
            self.sendButton.setEnabled(False)
            self.worker = ResponseWorker(message)
            self.worker.response_received.connect(self.append_message)
            self.worker.finished.connect(lambda: self.sendButton.setEnabled(True))
            self.worker.start()

    def append_message(self, sender, message):
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        sender_style = "color: #6cb2eb;" if sender == "You" else "color: #e3342f;"
        self.chatHistory.append(f"<b style='{sender_style}'>{sender}:</b> {message} <span style='color: grey; font-size: small;'>({timestamp})</span>")
        self.chatHistory.moveCursor(QTextCursor.End)

class ResponseWorker(QThread):
    response_received = pyqtSignal(str, str)
    finished = pyqtSignal()

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        try:
            for chunk in get_response_stream(self.message):
                self.response_received.emit("Llama3", chunk)
        except Exception as e:
            self.response_received.emit("Llama3", f"An error occurred: {e}")
        self.finished.emit()

