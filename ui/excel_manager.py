import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableView, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class ExcelManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Excel Files")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.loadButton = QPushButton("Load Excel File")
        self.loadButton.clicked.connect(self.load_excel)
        layout.addWidget(self.loadButton)

        self.tableView = QTableView()
        layout.addWidget(self.tableView)

        self.saveButton = QPushButton("Save Excel File")
        self.saveButton.clicked.connect(self.save_excel)
        layout.addWidget(self.saveButton)

        self.setLayout(layout)

    def load_excel(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if filePath:
            self.df = pd.read_excel(filePath)
            self.model = QStandardItemModel()
            self.model.setHorizontalHeaderLabels(self.df.columns.tolist())
            for row in self.df.values:
                items = [QStandardItem(str(item)) for item in row]
                self.model.appendRow(items)
            self.tableView.setModel(self.model)
        else:
            QMessageBox.warning(self, "Error", "No file selected")

    def save_excel(self):
        if hasattr(self, 'df'):
            filePath, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx *.xls)")
            if filePath:
                self.df.to_excel(filePath, index=False)
                QMessageBox.information(self, "Success", "File saved successfully")
            else:
                QMessageBox.warning(self, "Error", "No file selected")
        else:
            QMessageBox.warning(self, "Error", "No data to save")

