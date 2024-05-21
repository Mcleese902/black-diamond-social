from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QComboBox, QDateEdit, QMessageBox, QLabel, QTextEdit
from PyQt5.QtCore import Qt, QDate
import sqlite3

class TaskManager(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()
        self.create_table()
        self.load_tasks()

    def initUI(self):
        layout = QVBoxLayout()

        # Task input layout
        inputLayout = QVBoxLayout()

        # Task input
        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText("Enter a new task...")
        inputLayout.addWidget(QLabel("Task:"))
        inputLayout.addWidget(self.taskInput)

        # Task details input
        self.detailsInput = QTextEdit()
        self.detailsInput.setPlaceholderText("Enter task details...")
        inputLayout.addWidget(QLabel("Details:"))
        inputLayout.addWidget(self.detailsInput)

        # Category input
        self.categoryInput = QComboBox()
        self.categoryInput.addItems(["Work", "Personal", "Urgent", "Other"])
        inputLayout.addWidget(QLabel("Category:"))
        inputLayout.addWidget(self.categoryInput)

        # Due date input
        self.dueDateInput = QDateEdit()
        self.dueDateInput.setCalendarPopup(True)
        self.dueDateInput.setDate(QDate.currentDate())
        inputLayout.addWidget(QLabel("Due Date:"))
        inputLayout.addWidget(self.dueDateInput)

        # Priority input
        self.priorityInput = QComboBox()
        self.priorityInput.addItems(["Low", "Medium", "High"])
        inputLayout.addWidget(QLabel("Priority:"))
        inputLayout.addWidget(self.priorityInput)

        # Add and Edit task buttons
        buttonLayout = QHBoxLayout()
        self.addButton = QPushButton("Add Task")
        self.addButton.clicked.connect(self.add_task)
        buttonLayout.addWidget(self.addButton)

        self.editButton = QPushButton("Edit Task")
        self.editButton.clicked.connect(self.edit_task)
        buttonLayout.addWidget(self.editButton)

        inputLayout.addLayout(buttonLayout)

        layout.addLayout(inputLayout)

        # Task list
        self.taskList = QListWidget()
        self.taskList.itemClicked.connect(self.load_task_for_editing)
        layout.addWidget(QLabel("Tasks:"))
        layout.addWidget(self.taskList)

        # Filter and sort layout
        filterSortLayout = QHBoxLayout()

        # Category filter
        self.categoryFilter = QComboBox()
        self.categoryFilter.addItems(["All", "Work", "Personal", "Urgent", "Other"])
        self.categoryFilter.currentTextChanged.connect(self.load_tasks)
        filterSortLayout.addWidget(QLabel("Category:"))
        filterSortLayout.addWidget(self.categoryFilter)

        # Status filter
        self.statusFilter = QComboBox()
        self.statusFilter.addItems(["All", "Pending", "Completed"])
        self.statusFilter.currentTextChanged.connect(self.load_tasks)
        filterSortLayout.addWidget(QLabel("Status:"))
        filterSortLayout.addWidget(self.statusFilter)

        # Sort options
        self.sortOption = QComboBox()
        self.sortOption.addItems(["Due Date", "Priority", "Category"])
        self.sortOption.currentTextChanged.connect(self.load_tasks)
        filterSortLayout.addWidget(QLabel("Sort by:"))
        filterSortLayout.addWidget(self.sortOption)

        layout.addLayout(filterSortLayout)

        # Mark as completed button
        self.markCompletedButton = QPushButton("Mark as Completed")
        self.markCompletedButton.clicked.connect(self.mark_task_completed)
        layout.addWidget(self.markCompletedButton)

        self.setLayout(layout)

    def create_table(self):
        connection = sqlite3.connect('black_diamond_social.db')
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task TEXT NOT NULL,
                details TEXT,
                category TEXT,
                due_date TEXT,
                priority TEXT,
                status TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        connection.close()

    def load_tasks(self):
        connection = sqlite3.connect('black_diamond_social.db')
        cursor = connection.cursor()

        query = "SELECT id, task, category, due_date, priority, status FROM tasks WHERE user_id = ?"
        filters = [self.user_id]

        # Apply category filter
        if self.categoryFilter.currentText() != "All":
            query += " AND category = ?"
            filters.append(self.categoryFilter.currentText())

        # Apply status filter
        if self.statusFilter.currentText() != "All":
            query += " AND status = ?"
            filters.append(self.statusFilter.currentText())

        # Apply sorting
        if self.sortOption.currentText() == "Due Date":
            query += " ORDER BY due_date"
        elif self.sortOption.currentText() == "Priority":
            query += " ORDER BY priority"
        elif self.sortOption.currentText() == "Category":
            query += " ORDER BY category"

        cursor.execute(query, filters)
        tasks = cursor.fetchall()
        connection.close()
        
        self.taskList.clear()
        for task in tasks:
            task_item = f"{task[0]} | {task[1]} | Category: {task[2]} | Due: {task[3]} | Priority: {task[4]} | Status: {task[5]}"
            self.taskList.addItem(task_item)

    def add_task(self):
        task = self.taskInput.text().strip()
        details = self.detailsInput.toPlainText().strip()
        category = self.categoryInput.currentText()
        due_date = self.dueDateInput.date().toString(Qt.ISODate)
        priority = self.priorityInput.currentText()
        status = "Pending"

        if task:
            connection = sqlite3.connect('black_diamond_social.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO tasks (user_id, task, details, category, due_date, priority, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (self.user_id, task, details, category, due_date, priority, status))
            connection.commit()
            connection.close()
            self.load_tasks()
            self.taskInput.clear()
            self.detailsInput.clear()
        else:
            QMessageBox.warning(self, "Warning", "Task cannot be empty")

    def load_task_for_editing(self, item):
        task_id = item.text().split(" | ")[0]
        connection = sqlite3.connect('black_diamond_social.db')
        cursor = connection.cursor()
        cursor.execute("SELECT task, details, category, due_date, priority FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        connection.close()

        if task:
            self.current_task_id = task_id
            self.taskInput.setText(task[0])
            self.detailsInput.setText(task[1])
            self.categoryInput.setCurrentText(task[2])
            self.dueDateInput.setDate(QDate.fromString(task[3], Qt.ISODate))
            self.priorityInput.setCurrentText(task[4])

    def edit_task(self):
        if not self.current_task_id:
            QMessageBox.warning(self, "Warning", "Please select a task to edit")
            return

        task = self.taskInput.text().strip()
        details = self.detailsInput.toPlainText().strip()
        category = self.categoryInput.currentText()
        due_date = self.dueDateInput.date().toString(Qt.ISODate)
        priority = self.priorityInput.currentText()

        if task:
            connection = sqlite3.connect('black_diamond_social.db')
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE tasks SET task = ?, details = ?, category = ?, due_date = ?, priority = ?
                WHERE id = ?
            """, (task, details, category, due_date, priority, self.current_task_id))
            connection.commit()
            connection.close()
            self.load_tasks()
            self.taskInput.clear()
            self.detailsInput.clear()
            self.current_task_id = None
        else:
            QMessageBox.warning(self, "Warning", "Task cannot be empty")

    def remove_task(self, item):
        task_id = item.text().split(" | ")[0]
        connection = sqlite3.connect('black_diamond_social.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        connection.commit()
        connection.close()
        self.taskList.takeItem(self.taskList.row(item))

    def show_task_details(self, item):
        task_id = item.text().split(" | ")[0]
        connection = sqlite3.connect('black_diamond_social.db')
        cursor = connection.cursor()
        cursor.execute("SELECT details FROM tasks WHERE id = ?", (task_id,))
        details = cursor.fetchone()
        connection.close()
        if details:
            QMessageBox.information(self, "Task Details", details[0])

    def mark_task_completed(self):
        selected_items = self.taskList.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a task to mark as completed")
            return

        task_id = selected_items[0].text().split(" | ")[0]
        connection = sqlite3.connect('black_diamond_social.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
        connection.commit()
        connection.close()
        self.load_tasks()

