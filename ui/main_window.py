from PyQt5.QtWidgets import QMainWindow, QAction, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QMessageBox
from ui.chat_window import ChatWindow
from ui.task_manager import TaskManager
from ui.user_profile import UserProfile
from ui.news_feed import NewsFeed
from ui.friends_list import FriendsList
from ui.coworkers_list import CoworkersList

class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Black Diamond Social")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()
        self.opened_windows = []  # To track opened windows

    def initUI(self):
        mainMenu = self.menuBar()
        
        # File menu
        fileMenu = mainMenu.addMenu('File')

        logOutAction = QAction('Log Out', self)
        logOutAction.triggered.connect(self.log_out)
        fileMenu.addAction(logOutAction)

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # Tools menu
        toolsMenu = mainMenu.addMenu('Tools')

        chatAction = QAction('Chat with Llama3', self)
        chatAction.triggered.connect(self.open_chat_window)
        toolsMenu.addAction(chatAction)

        taskManagerAction = QAction('Task Manager', self)
        taskManagerAction.triggered.connect(self.open_task_manager)
        toolsMenu.addAction(taskManagerAction)

        profileAction = QAction('User Profile', self)
        profileAction.triggered.connect(self.open_user_profile)
        toolsMenu.addAction(profileAction)

        # Social menu
        socialMenu = mainMenu.addMenu('Social')

        newsFeedAction = QAction('News Feed', self)
        newsFeedAction.triggered.connect(self.open_news_feed)
        socialMenu.addAction(newsFeedAction)

        friendsListAction = QAction('Friends List', self)
        friendsListAction.triggered.connect(self.open_friends_list)
        socialMenu.addAction(friendsListAction)

        coworkersListAction = QAction('Co-Workers List', self)
        coworkersListAction.triggered.connect(self.open_coworkers_list)
        socialMenu.addAction(coworkersListAction)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout()
        
        buttonLayout = QHBoxLayout()

        self.chatButton = QPushButton('Chat')
        self.chatButton.clicked.connect(self.open_chat_window)
        buttonLayout.addWidget(self.chatButton)

        self.taskManagerButton = QPushButton('Tasks')
        self.taskManagerButton.clicked.connect(self.open_task_manager)
        buttonLayout.addWidget(self.taskManagerButton)

        self.profileButton = QPushButton('Profile')
        self.profileButton.clicked.connect(self.open_user_profile)
        buttonLayout.addWidget(self.profileButton)

        self.newsFeedButton = QPushButton('News Feed')
        self.newsFeedButton.clicked.connect(self.open_news_feed)
        buttonLayout.addWidget(self.newsFeedButton)

        self.friendsListButton = QPushButton('Friends List')
        self.friendsListButton.clicked.connect(self.open_friends_list)
        buttonLayout.addWidget(self.friendsListButton)

        self.coworkersListButton = QPushButton('Co-Workers List')
        self.coworkersListButton.clicked.connect(self.open_coworkers_list)
        buttonLayout.addWidget(self.coworkersListButton)

        layout.addLayout(buttonLayout)
        self.central_widget.setLayout(layout)

        self.show()

    def open_chat_window(self):
        self.close_opened_windows()
        self.chat_window = ChatWindow()
        self.chat_window.show()
        self.opened_windows.append(self.chat_window)

    def open_task_manager(self):
        self.close_opened_windows()
        self.task_manager = TaskManager(self.user_id)
        self.task_manager.show()
        self.opened_windows.append(self.task_manager)

    def open_user_profile(self):
        self.close_opened_windows()
        self.user_profile = UserProfile(self.user_id)
        self.user_profile.show()
        self.opened_windows.append(self.user_profile)

    def open_news_feed(self):
        self.close_opened_windows()
        self.news_feed = NewsFeed(self.user_id)
        self.news_feed.show()
        self.opened_windows.append(self.news_feed)

    def open_friends_list(self):
        self.close_opened_windows()
        self.friends_list = FriendsList(self.user_id)
        self.friends_list.show()
        self.opened_windows.append(self.friends_list)

    def open_coworkers_list(self):
        self.close_opened_windows()
        self.coworkers_list = CoworkersList(self.user_id)
        self.coworkers_list.show()
        self.opened_windows.append(self.coworkers_list)

    def close_opened_windows(self):
        for window in self.opened_windows:
            window.close()
        self.opened_windows.clear()

    def log_out(self):
        self.close_opened_windows()
        self.close()
        from ui.start_window import StartWindow  # Local import to avoid circular dependency
        self.start_window = StartWindow()
        self.start_window.show()

    def show_about(self):
        about_text = ("Black Diamond Social\n\n"
                      "Version 1.0\n\n"
                      "This application is designed to provide a social hub, "
                      "including a news feed, status updates, user profiles, "
                      "friends, and co-workers.")
        QMessageBox.about(self, "About Black Diamond Social", about_text)

